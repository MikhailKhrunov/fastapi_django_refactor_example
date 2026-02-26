from fastapi import APIRouter, HTTPException, status
from typing import List
import datetime as dt
from schemas.cats import CatCreate, CatUpdate, CatResponse
from schemas.achievements import AchievementResponse
from api.users import _users_db
from api.achievements import _achievements_db, _next_achievement_id

router = APIRouter()

_cats_db: List[CatResponse] = []
_next_cat_id: int = 1


def _calculate_age(birth_year: int) -> int: # расчитывает возраст
    return dt.datetime.now().year - birth_year

def _get_user_by_id(user_id: int): # вспомогательная для поиска пользователя
    return next((u for u in _users_db if u.id == user_id), None)

@router.get("/cats", response_model=List[CatResponse])
async def get_cats(): # получить всех
    return _cats_db

@router.get("/cats/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int): # получить по айди
    cat = next((c for c in _cats_db if c.id == cat_id), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Кот не найден")
    return cat

@router.post("/cats", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(cat: CatCreate): # создание котика :)
    global _next_cat_id, _next_achievement_id
    owner = _get_user_by_id(cat.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Владелец не найден")
    achievements = []
    if cat.achievements:
        for ach_name in cat.achievements:
            existing = next((a for a in _achievements_db if a.name == ach_name), None)
            if existing:
                achievements.append(existing.achievement_name)
            else:
                new_ach = AchievementResponse(
                    id=_next_achievement_id,
                    name=ach_name,
                    achievement_name=ach_name
                )
                _achievements_db.append(new_ach)
                achievements.append(ach_name)
                _next_achievement_id += 1
    new_cat = CatResponse(
        id=_next_cat_id,
        name=cat.name,
        color=cat.color,
        birth_year=cat.birth_year,
        owner_id=cat.owner_id,
        achievements=achievements,
        age=_calculate_age(cat.birth_year)
    )
    _cats_db.append(new_cat)
    if owner:
        owner.cats.append(cat.name)
    _next_cat_id += 1
    return new_cat

@router.put("/cats/{cat_id}", response_model=CatResponse)
async def update_cat(cat_id: int, cat: CatUpdate): # обновление кота
    db_cat = next((c for c in _cats_db if c.id == cat_id), None)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Кот не найден")
    update_data = cat.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if field == 'birth_year':
                db_cat.age = _calculate_age(value)
            setattr(db_cat, field, value)
    if 'achievements' in update_data and update_data['achievements'] is not None:
        db_cat.achievements = update_data['achievements'] or []
    return db_cat

@router.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int): # удаление котика(
    global _cats_db
    cat = next((c for c in _cats_db if c.id == cat_id), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Кот не найден")
    owner = _get_user_by_id(cat.owner_id)
    if owner and cat.name in owner.cats:
        owner.cats.remove(cat.name)
    _cats_db = [c for c in _cats_db if c.id != cat_id]
    return None
