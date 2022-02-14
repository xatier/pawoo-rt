import logging
import os
import re
from typing import Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
    return logging.getLogger(name)


LOGGER = get_logger(__name__)

TWITTER_STATUS_REGEX = r'https://twitter.com/(\w+)/status/(\d+)'
EMBED_API = 'https://publish.twitter.com/oembed?url={url}&omit_script=true'

TOKEN = os.environ.get('TOKEN', '5566')
LOGGER.info(f'TOKEN: {TOKEN}')


class Payload(BaseModel):
    status: str
    token: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def validate(status: str, token: str) -> bool:
    if token != TOKEN:
        return False
    return bool(re.match(TWITTER_STATUS_REGEX, status))


def invalid() -> None:
    LOGGER.warning('/do ...invalid')
    raise HTTPException(status_code=500, detail="q_q")


def process(status: str) -> Dict[str, str] | None:
    r: httpx.Response = httpx.get(EMBED_API.format(url=status))
    if r.status_code != httpx.codes.OK:
        invalid()

    j = r.json()
    html: str = j.get('html', '')
    if m := re.search(
        r'<p(.+?)>(.+?)<\/p>',
        html,
    ):
        tweet = m.group(2)
        tweet = re.sub(r'<br>', '\n', tweet)
        tweet = re.sub(r'(pic.twitter.com/\w{,15})', r'https://\1', tweet)
        tweet = re.sub(r'<.+?>', ' ', tweet)
        LOGGER.info(f'{status} ->\n{tweet}')

        return {'status': tweet}

    invalid()
    return None  # unreachable


@app.post("/do", status_code=status.HTTP_200_OK)
def do(payload: Payload) -> Dict[str, str] | None:
    LOGGER.info('/do ...start')

    status, token = payload.status, payload.token

    if not validate(status, token):
        LOGGER.warning('/do ...invalid')
        raise HTTPException(status_code=403, detail="^q^")

    return process(status)
