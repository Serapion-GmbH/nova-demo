from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from nova_demo.services.chat_session_service import ChatSessionService
from nova_demo.settings import SHARED_SETTINGS

_client_session_indices_created = False

_mongo_client: AsyncIOMotorClient | None = None


async def get_db_client():
    global _mongo_client

    mongo_uri = SHARED_SETTINGS.db.uri.get_secret_value()
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(mongo_uri, uuidRepresentation="standard", tz_aware=True)
    return _mongo_client


async def get_database(client: Annotated[AsyncIOMotorClient, Depends(get_db_client)]):
    return client[SHARED_SETTINGS.db.database_name]


async def get_chat_session_service(
        db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
):
    global _client_session_indices_created
    service = ChatSessionService(db['client_sessions'])
    if not _client_session_indices_created:
        await service.create_indices()
        _client_session_indices_created = True

    return service
