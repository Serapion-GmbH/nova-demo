from typing import Annotated

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from starlette.requests import Request

from nova_demo.settings import SHARED_SETTINGS


class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request):
        return await super().__call__(request)


def check_token(
        bearer_token: Annotated[HTTPAuthorizationCredentials, Security(TokenBearer())],
):
    token = SHARED_SETTINGS.token.get_secret_value(),
    if bearer_token.credentials != token[0]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": 'unauthorized',
                "message": "You are not authorized to access this resource.",
            },
        )
