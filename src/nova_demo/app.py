from fastapi import FastAPI

from . import __version__ as nova_demo_version
from .routers.chat import router


def create_app():
    app = FastAPI()

    app.include_router(router)

    @app.get("/")
    @app.get("/health")
    async def health():
        return {
            "name": "nova_demo",
            "status": "ok",
            "version": nova_demo_version,
        }

    return app
