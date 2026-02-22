FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /usr/local/bin/uv

RUN mkdir /opt/remo2mqtt
WORKDIR /opt/remo2mqtt
COPY pyproject.toml .
COPY uv.lock .
COPY .python-version .
COPY remo2mqtt.py .
COPY remo_scanner.py .
COPY mqtt_publisher.py .

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "remo2mqtt.py"]