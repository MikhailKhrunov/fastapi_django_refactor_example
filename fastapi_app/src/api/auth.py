from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, SecretStr
from datetime import timedelta

from database import database
from infrastructure.repositories.users import UserRepository
from core.jwt import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    with database.session() as session:
        repo = UserRepository(session)
        user = repo.get_by_username(request.username)

        if not user or not repo.verify_password(
            user,
            request.password.get_secret_value()
        ):
            raise HTTPException(
                status_code=401,
                detail="Неверный логин или пароль"
            )

        token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=timedelta(minutes=30)
        )

        return TokenResponse(access_token=token, token_type="bearer")


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def register(request: LoginRequest):
    with database.session() as session:
        repo = UserRepository(session)

        if repo.get_by_username(request.username):
            raise HTTPException(
                status_code=400,
                detail="Пользователь уже существует"
            )

        user = repo.create(
            username=request.username,
            password=request.password.get_secret_value()
        )

        return {"id": user.id, "username": user.username}
