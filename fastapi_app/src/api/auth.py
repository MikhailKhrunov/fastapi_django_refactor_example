from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, SecretStr
from datetime import timedelta
import logging
from core.logging_config import log_user_action
from database import database
from infrastructure.repositories.users import UserRepository
from core.jwt import create_access_token
from schemas.errors import ErrorResponse, ValidationErrorResponse

router = APIRouter()
logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    username: str
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        200: {"model": TokenResponse},
        400: {"model": ErrorResponse},
        401: {
            "model": ErrorResponse,
        },
        422: {
            "model": ValidationErrorResponse,
        },
        500: {
            "model": ErrorResponse,
        },
    }
)
async def login(request: LoginRequest):
    with database.session() as session:
        repo = UserRepository(session)
        user = repo.get_by_username(request.username)

        if not user or not repo.verify_password(
            user,
            request.password.get_secret_value()
        ):
            logger.warning(
                f"Failed login attempt for username: {request.username}"
            )
            raise HTTPException(
                status_code=401,
                detail="Неверный логин или пароль"
            )

        token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=timedelta(minutes=30)
        )
        log_user_action(user.id, "USER_LOGIN", {"username": user.username})
        logger.info(f"User {user.username} logged in successfully")

        return TokenResponse(access_token=token, token_type="bearer")


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Created"},
        400: {
            "model": ErrorResponse,
        },
        422: {
            "model": ValidationErrorResponse,
        },
        500: {
            "model": ErrorResponse,
        },
    }
)
async def register(request: LoginRequest):
    with database.session() as session:
        repo = UserRepository(session)

        if repo.get_by_username(request.username):
            logger.warning(
                f"Registration try with existing username: {request.username}"
            )
            raise HTTPException(
                status_code=400,
                detail="Пользователь уже существует"
            )

        user = repo.create(
            username=request.username,
            password=request.password.get_secret_value()
        )
        log_user_action(user.id, "USER_REGISTER", {"username": user.username})
        logger.info(f"New user registered: {user.username}")

        return {"id": user.id, "username": user.username}
