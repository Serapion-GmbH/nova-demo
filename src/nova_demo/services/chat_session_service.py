from uuid import UUID, uuid4

from motor.motor_asyncio import AsyncIOMotorCollection

from nova_demo.models.message import Message


class ChatSessionService():
    def __init__(self, collection: AsyncIOMotorCollection):
        self.__collection = collection

    async def create_indices(self):
        await self.__collection.create_index("message_id", unique=True)

    async def __create_message_id(self) -> UUID:
        message_id = uuid4()
        while await self.__collection.find_one({"message_id": message_id}):
            message_id = uuid4()
        return message_id

    async def create_message(
        self,
        message: Message,
    ):
        await self.__collection.insert_one(
            {
                "message_id": await self.__create_message_id(),
                "role": message.role,
                "message": message.message,
            }
        )