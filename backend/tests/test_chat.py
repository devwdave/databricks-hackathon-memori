from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from openai import OpenAIError

from app.core.config import Settings
from app.core.deps import get_openai_client, get_settings
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_openai_client() -> MagicMock:
    return MagicMock()


@pytest.fixture(autouse=True)
def override_dependencies(mock_openai_client: MagicMock):
    app.dependency_overrides[get_openai_client] = lambda: mock_openai_client
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        openai_api_key="test-key",
        memori_api_key="test-key",
        openai_model="gpt-4o-mini",
        cors_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    )
    yield
    app.dependency_overrides.clear()


def test_create_chat_message(mock_openai_client: MagicMock) -> None:
    mock_choice = MagicMock()
    mock_choice.message.content = "Hello back"
    mock_openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[mock_choice]),
    )

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"reply": "Hello back"}
    mock_openai_client.chat.completions.create.assert_awaited_once_with(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}],
    )


def test_create_chat_message_rejects_empty_message() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": ""},
    )

    assert response.status_code == 422


def test_create_chat_message_rejects_missing_message() -> None:
    response = client.post("/api/v1/chat", json={})

    assert response.status_code == 422


def test_create_chat_message_returns_empty_reply_when_openai_content_is_none(
    mock_openai_client: MagicMock,
) -> None:
    mock_choice = MagicMock()
    mock_choice.message.content = None
    mock_openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[mock_choice]),
    )

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"reply": ""}


def test_create_chat_message_returns_502_when_openai_fails(
    mock_openai_client: MagicMock,
) -> None:
    mock_openai_client.chat.completions.create = AsyncMock(
        side_effect=OpenAIError("upstream failure"),
    )

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Failed to generate reply from language model",
    }


def test_cors_allows_configured_origin_preflight() -> None:
    response = client.options(
        "/api/v1/chat",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_does_not_allow_unlisted_origin(mock_openai_client: MagicMock) -> None:
    mock_choice = MagicMock()
    mock_choice.message.content = "Hello back"
    mock_openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[mock_choice]),
    )

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
        headers={"Origin": "http://evil.example"},
    )

    assert response.headers.get("access-control-allow-origin") != "http://evil.example"
