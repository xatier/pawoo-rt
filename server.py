import html
import logging
import os
import re
from typing import Dict

import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
    return logging.getLogger(name)


LOGGER: logging.Logger = get_logger(__name__)

TWITTER_STATUS_REGEX: str = r'https://(mobile\.)?(twitter|x).com/(\w+)/status/(\d+)'
EMBED_API: str = 'https://publish.twitter.com/oembed?url={url}&omit_script=true'

TOKEN: str = os.environ.get('TOKEN', '5566')
LOGGER.info(f'TOKEN: {TOKEN}')


class Payload(BaseModel):
    status: str
    token: str


app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def validate_token(status: str, token: str) -> bool:
    return token == TOKEN


def is_tweet(status: str) -> bool:
    return bool(re.match(TWITTER_STATUS_REGEX, status))


def invalid() -> None:
    LOGGER.warning('/do ...invalid')
    raise HTTPException(status_code=500, detail="q_q")


def get_title(status: str) -> Dict[str, str] | None:
    try:
        text: str = httpx.get(
            status, headers={
                'user-agent': 'Mozilla/5.0 Chrome/102.0.4985.0'
            }
        ).text
        title: str = text[text.find('<title>') +
                          len('<title>'):text.find('</title>')]
        LOGGER.info(f'{status} ->\n{title}')
        return {'status': title}
    except httpx.HTTPError as e:
        LOGGER.warning(f'HTTP error on "{status}", {e}')

    invalid()
    return None  # unreachable


def process_tweet(html_text: str) -> str | None:
    html_text = html.unescape(html_text)
    if m := re.search(
        r'<p(.+?)>(.+?)<\/p>',
        html_text,
    ):
        tweet = m[2]
        tweet = re.sub(r'<br>', '\n', tweet)
        tweet = re.sub(r'(pic.twitter.com/\w{,15})', r'https://\1', tweet)
        return re.sub(r'<.+?>', ' ', tweet)

    return None


def process(status: str) -> Dict[str, str] | None:
    # fetch page title if it's not a tweet
    if not is_tweet(status):
        return get_title(status)

    # EMBED_API only works with twitter.com
    if 'x.com' in status:
        status = status.replace('x.com', 'twitter.com')

    r: httpx.Response = httpx.get(EMBED_API.format(url=status))
    if r.status_code != httpx.codes.OK:
        invalid()

    j = r.json()
    html_text: str = j.get('html', '')
    if tweet := process_tweet(html_text):
        LOGGER.info(f'{status} ->\n{tweet}')
        return {'status': tweet}

    invalid()
    return None  # unreachable


@app.post("/do", status_code=status.HTTP_200_OK)
def do(payload: Payload) -> Dict[str, str] | None:
    LOGGER.info('/do ...start')

    status, token = payload.status, payload.token

    if not validate_token(status, token):
        LOGGER.warning(f'/do ...invalid token {token}')
        raise HTTPException(status_code=403, detail="^q^")

    # trim 'mobile' prefix
    status = status.replace('mobile.twitter.com', 'twitter.com', 1)

    return process(status)
