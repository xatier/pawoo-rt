FROM ghcr.io/xatier/arch-dev:latest

USER root
RUN pacman -Syuu --noconfirm --needed \
    python

WORKDIR /app
RUN chown xatier:xatier /app

ENV TOKEN=5566
USER xatier

COPY ./requirements.txt /app/requirements.txt
COPY ./server.py /app/server.py

RUN python -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["bash", "-c", "source venv/bin/activate && exec uvicorn server:app --reload --port 5566"]
