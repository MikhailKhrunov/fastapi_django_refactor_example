from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.base import router as base_router
from api.cats import router as cats_router
from api.users import router as users_router
from api.achievements import router as achievements_router

def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    app.include_router(cats_router, prefix="/cats", tags=["Cats"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(achievements_router, prefix="/achievements", tags=["Achievements"])

    return app
