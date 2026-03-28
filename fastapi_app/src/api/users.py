from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.users import UserCreate, UserUpdate, UserResponse

router = APIRouter()

_users_db: List[UserResponse] = []
_next_user_id: int = 1


@router.get("/", response_model=List[UserResponse])
async def get_users():  # получаем всех
    return _users_db


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):  # получение по ID
    user = next((u for u in _users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User не найден")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):  # создание нового
    global _next_user_id
    if any(u.username == user.username for u in _users_db):
        raise HTTPException(
            status_code=400, detail="User с таким именем уже существует"
        )
    new_user = UserResponse(
        id=_next_user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        cats=[],
    )
    _users_db.append(new_user)
    _next_user_id += 1
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):  # обновление
    db_user = next((u for u in _users_db if u.id == user_id), None)
    if not db_user:
        raise HTTPException(status_code=404, detail="User не найден")
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_user, field, value)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):  # удаление
    global _users_db
    user = next((u for u in _users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User не найден")

    _users_db = [u for u in _users_db if u.id != user_id]
    return None
