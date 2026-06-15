from fastapi import HTTPException, status
from openai import AsyncOpenAI, OpenAIError

from app.core.config import Settings


async def generate_reply(
    message: str,
    *,
    client: AsyncOpenAI,
    settings: Settings,
) -> str:
    """Generate a reply for the given user message."""
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": message}],
        )
    except OpenAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to generate reply from language model",
        ) from exc

    if not response.choices:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Empty response from language model",
        )

    return response.choices[0].message.content or ""
