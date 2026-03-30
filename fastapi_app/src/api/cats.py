from fastapi import APIRouter, Depends, status
from core.dependencies import get_current_user
from domain.user.usecases.cat import CatUseCase
from schemas.cats import CatCreate, CatUpdate, CatResponse
# импорты через (), из-за flake8
from core.exceptions.api_exceptions import (
    NotFoundException,
    BadRequestException,
    InternalServerException,
)
from core.exceptions.domain_exceptions import (
    EntityNotFoundError,
    OwnerNotFoundError,
    DomainError,
)

router = APIRouter()
usecase = CatUseCase()


@router.get("/", response_model=list[CatResponse])
async def get_cats(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    try:
        return usecase.get_all(skip=skip, limit=limit)
    except DomainError as e:
        raise InternalServerException(
            e.message,
            {"code": e.error_code, **e.details}
        )


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int, current_user: dict = Depends(get_current_user)):
    try:
        cat = usecase.get_by_id(cat_id)
        if not cat:
            raise NotFoundException(
                f"Кот с ID {cat_id} не найден",
                {"cat_id": cat_id}
            )
        return cat
    except EntityNotFoundError as e:
        raise NotFoundException(e.message, {"code": e.error_code, **e.details})
    except DomainError as e:
        raise InternalServerException(
            e.message,
            {"code": e.error_code, **e.details}
        )


@router.post(
    "/",
    response_model=CatResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_cat(
    cat: CatCreate,
    current_user: dict = Depends(get_current_user)
):
    try:
        cat.owner_id = current_user["user_id"]
        return usecase.create(cat)
    except OwnerNotFoundError as e:
        raise NotFoundException(e.message, {"code": e.error_code, **e.details})
    except DomainError as e:
        if e.error_code == "CAT_CREATE_ERROR":
            raise BadRequestException(
                e.message,
                {"code": e.error_code, **e.details}
            )
        raise InternalServerException(
            e.message,
            {"code": e.error_code, **e.details}
        )


@router.put("/{cat_id}", response_model=CatResponse)
async def update_cat(
    cat_id: int,
    cat: CatUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        updated = usecase.update(cat_id, cat)
        if not updated:
            raise NotFoundException(
                f"Кот с ID {cat_id} не найден",
                {"cat_id": cat_id}
            )
        return updated
    except EntityNotFoundError as e:
        raise NotFoundException(e.message, {"code": e.error_code, **e.details})
    except DomainError as e:
        raise InternalServerException(
            e.message,
            {"code": e.error_code, **e.details}
        )


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(
    cat_id: int,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not usecase.delete(cat_id):
            raise NotFoundException(
                f"Кот с ID {cat_id} не найден",
                {"cat_id": cat_id}
            )
        return None
    except EntityNotFoundError as e:
        raise NotFoundException(e.message, {"code": e.error_code, **e.details})
    except DomainError as e:
        raise InternalServerException(
            e.message,
            {"code": e.error_code, **e.details}
        )
