import os
import socket
import time

import redis
from flask import Flask


app = Flask(__name__)


def redis_client() -> redis.Redis:
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "db-service"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
    )


def increment_hits(client: redis.Redis, retries: int = 10) -> int:
    last_error = None
    for attempt in range(retries):
        try:
            return int(client.incr("hits"))
        except redis.RedisError as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(1)
    raise RuntimeError("Redis is unavailable") from last_error


@app.get("/")
def home() -> str:
    hits = increment_hits(redis_client())
    container_id = socket.gethostname()
    return f"Bonjour ! Cette page a été vue {hits} fois. Je suis le conteneur {container_id}"


@app.get("/health")
def health() -> tuple[str, int]:
    try:
        redis_client().ping()
    except redis.RedisError:
        return "unhealthy", 503
    return "healthy", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
