from fastapi import APIRouter, HTTPException, status

from usecases.cat import CatUseCase
from schemas.cats import CatCreate, CatUpdate, CatResponse

router = APIRouter()
usecase = CatUseCase()


@router.get("/", response_model=list[CatResponse])
async def get_cats(skip: int = 0, limit: int = 100):
    """Получить всех котов"""
    return usecase.get_all(skip=skip, limit=limit)


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int):
    """Получить кота по ID"""
    cat = usecase.get_by_id(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Кот не найден")
    return cat


@router.post(
    "/",
    response_model=CatResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_cat(cat: CatCreate):
    """Создать кота"""
    return usecase.create(cat)


@router.put("/{cat_id}", response_model=CatResponse)
async def update_cat(cat_id: int, cat: CatUpdate):
    """Обновить кота"""
    updated = usecase.update(cat_id, cat)
    if not updated:
        raise HTTPException(status_code=404, detail="Кот не найден")
    return updated


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int):
    """Удалить кота"""
    if not usecase.delete(cat_id):
        raise HTTPException(status_code=404, detail="Кот не найден")
    return None
