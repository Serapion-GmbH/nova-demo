import re
from typing import Literal, Annotated

from fastapi import APIRouter, Security, Depends, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from nova_demo.models.message import Message
from nova_demo.provider.chat_session_provider import get_chat_session_service
from nova_demo.provider.check_token import check_token
from nova_demo.services.chat_session_service import ChatSessionService
from nova_demo.settings import SHARED_SETTINGS

router = APIRouter(prefix="/chat")


class ChatResponse(BaseModel):
    role: Literal["assistant"] = "assistant"
    message: str


@router.post("", response_model=ChatResponse, dependencies=[Security(check_token)])
async def create_session(
        user_message: str,
        chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)],
):
    await chat_session_service.create_message(Message(role='user', message=user_message))

    client = AsyncOpenAI(
        api_key=SHARED_SETTINGS.openai.api_key.get_secret_value(),
    )

    messages = [
        {
            'role': 'user',
            'content': user_message
        }
    ]

    args = {
        'messages': messages,
        'temperature': 0.7,
        'model': 'gpt-3.5-turbo',
    }

    response = await client.chat.completions.create(stream=False, **args)
    response_message = response.choices[0].message.content
    await chat_session_service.create_message(Message(role='assistant', message=response_message))

    return ChatResponse(message=response_message)
