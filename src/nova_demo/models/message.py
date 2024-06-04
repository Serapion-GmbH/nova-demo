from typing import Literal
from uuid import uuid4, UUID

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    message: str
