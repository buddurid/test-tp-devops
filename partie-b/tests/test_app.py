from unittest.mock import Mock

import redis

from app import app, increment_hits


def test_home_displays_counter_and_container_id(monkeypatch):
    client = Mock()
    client.incr.return_value = 7
    monkeypatch.setattr("app.redis_client", lambda: client)
    monkeypatch.setattr("app.socket.gethostname", lambda: "test-container")

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.text == (
        "Bonjour ! Cette page a été vue 7 fois. Je suis le conteneur test-container"
    )
    client.incr.assert_called_once_with("hits")


def test_increment_hits_retries_when_redis_is_temporarily_unavailable():
    client = Mock()
    client.incr.side_effect = [redis.ConnectionError(), 3]

    assert increment_hits(client, retries=2) == 3
