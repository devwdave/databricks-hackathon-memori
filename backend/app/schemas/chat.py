from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="User message to send to the API",
    )


class ChatResponse(BaseModel):
    reply: str = Field(..., description="API reply")
