from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.achievements import AchievementCreate, AchievementResponse

router = APIRouter()

_achievements_db: List[AchievementResponse] = []
_next_achievement_id: int = 1


@router.get("/", response_model=List[AchievementResponse])
async def get_achievements():  # получение
    return _achievements_db


@router.get("/{achievement_id}", response_model=AchievementResponse)
async def get_achievement(achievement_id: int):  # получение по айди
    achievement = next((a for a in _achievements_db if a.id == achievement_id), None)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    return achievement


@router.post(
    "/",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_achievement(achievement: AchievementCreate):  # создание
    global _next_achievement_id
    existing = next((a for a in _achievements_db if a.name == achievement.name), None)
    if existing:
        return existing
    new_achievement = AchievementResponse(
        id=_next_achievement_id,
        name=achievement.name,
        achievement_name=achievement.name,
    )
    _achievements_db.append(new_achievement)
    _next_achievement_id += 1
    return new_achievement


@router.put("/{achievement_id}", response_model=AchievementResponse)
async def update_achievement(achievement_id: int, achievement: AchievementCreate):
    # обновление
    db_achievement = next((a for a in _achievements_db if a.id == achievement_id), None)
    if not db_achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    if achievement.name != db_achievement.name:
        exists = next(
            (
                a
                for a in _achievements_db
                if a.name == achievement.name and a.id != achievement_id
            ),
            None,
        )
        if exists:
            raise HTTPException(
                status_code=400, detail="Достижение с таким названием уже существует"
            )
        db_achievement.name = achievement.name
        db_achievement.achievement_name = achievement.name
    return db_achievement


@router.delete("/achievements/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(achievement_id: int):  # удаление
    global _achievements_db
    achievement = next((a for a in _achievements_db if a.id == achievement_id), None)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено")
    _achievements_db = [a for a in _achievements_db if a.id != achievement_id]
    return None
