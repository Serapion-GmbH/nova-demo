FROM python:3.12-slim-bookworm

COPY . /app
WORKDIR /app

RUN pip install .

ENV HOST=0.0.0.0
ENV PORT=8000

CMD uvicorn --host $HOST --port $PORT --log-level info --factory nova_demo.app:create_app
