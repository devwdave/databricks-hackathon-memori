from typing import Annotated

from fastapi import APIRouter, Depends
from openai import AsyncOpenAI

from app.core.config import Settings
from app.core.deps import get_openai_client, get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import generate_reply

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def create_chat_message(
    request: ChatRequest,
    settings: Annotated[Settings, Depends(get_settings)],
    openai_client: Annotated[AsyncOpenAI, Depends(get_openai_client)],
) -> ChatResponse:
    reply = await generate_reply(
        request.message,
        client=openai_client,
        settings=settings,
    )
    return ChatResponse(reply=reply)
