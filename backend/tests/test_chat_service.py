from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from openai import AsyncOpenAI, OpenAIError

from app.core.config import Settings
from app.services.chat import generate_reply


@pytest.fixture
def settings() -> Settings:
    return Settings(
        _env_file=None,
        openai_api_key="test-key",
        memori_api_key="test-key",
        openai_model="gpt-4o-mini",
    )


@pytest.fixture
def openai_client() -> MagicMock:
    return MagicMock(spec=AsyncOpenAI)


@pytest.mark.asyncio
async def test_generate_reply_sends_message_to_openai(
    openai_client: MagicMock,
    settings: Settings,
) -> None:
    mock_choice = MagicMock()
    mock_choice.message.content = "Agent reply"
    openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[mock_choice]),
    )

    reply = await generate_reply(
        "Hello",
        client=openai_client,
        settings=settings,
    )

    assert reply == "Agent reply"
    openai_client.chat.completions.create.assert_awaited_once_with(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}],
    )


@pytest.mark.asyncio
async def test_generate_reply_returns_empty_string_when_content_is_none(
    openai_client: MagicMock,
    settings: Settings,
) -> None:
    mock_choice = MagicMock()
    mock_choice.message.content = None
    openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[mock_choice]),
    )

    reply = await generate_reply(
        "Hello",
        client=openai_client,
        settings=settings,
    )

    assert reply == ""


@pytest.mark.asyncio
async def test_generate_reply_raises_502_when_openai_fails(
    openai_client: MagicMock,
    settings: Settings,
) -> None:
    openai_client.chat.completions.create = AsyncMock(
        side_effect=OpenAIError("upstream failure"),
    )

    with pytest.raises(HTTPException) as exc_info:
        await generate_reply(
            "Hello",
            client=openai_client,
            settings=settings,
        )

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "Failed to generate reply from language model"


@pytest.mark.asyncio
async def test_generate_reply_raises_502_when_choices_are_empty(
    openai_client: MagicMock,
    settings: Settings,
) -> None:
    openai_client.chat.completions.create = AsyncMock(
        return_value=MagicMock(choices=[]),
    )

    with pytest.raises(HTTPException) as exc_info:
        await generate_reply(
            "Hello",
            client=openai_client,
            settings=settings,
        )

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "Empty response from language model"
