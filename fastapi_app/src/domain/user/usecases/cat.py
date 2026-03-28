from typing import List, Optional

from database import database
from infrastructure.repositories.cats import CatRepository
from infrastructure.models.cat_model import Cat as CatModel
from schemas.cats import CatCreate, CatUpdate, CatResponse
from core.exceptions.database_exceptions import (
    RecordNotFoundError,
    ForeignKeyError,
    DatabaseOperationError,
)
# импорты через (), из-за flake8
from core.exceptions.domain_exceptions import (
    EntityNotFoundError,
    OwnerNotFoundError,
    DomainError,
)


class CatUseCase:
    def __init__(self):
        self._database = database

    @staticmethod
    def _to_response(cat: CatModel) -> CatResponse:
        return CatResponse(
            id=cat.id,
            name=cat.name,
            color=cat.color,
            birth_year=cat.birth_year,
            owner_id=cat.owner_id,
            achievements=cat.get_achievements_list(),
            age=cat.age,
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CatResponse]:
        try:
            with self._database.session() as session:
                repo = CatRepository(session)
                cats = repo.get_all(skip=skip, limit=limit)
                return [self._to_response(cat) for cat in cats]
        except DatabaseOperationError as e:
            raise DomainError(
                "Не удалось получить список котов",
                "CATS_LIST_ERROR",
                {"error": str(e.original_error)}
            )

    def get_by_id(self, cat_id: int) -> Optional[CatResponse]:
        try:
            with self._database.session() as session:
                repo = CatRepository(session)
                cat = repo.get_by_id(cat_id)
                return self._to_response(cat) if cat else None
        except RecordNotFoundError as e:
            raise EntityNotFoundError(
                "Cat",
                cat_id,
                {"original": str(e.original_error)}
            )
        except DatabaseOperationError as e:
            raise DomainError(
                f"Не удалось получить кота {cat_id}",
                "CAT_GET_ERROR",
                {"error": str(e.original_error)}
            )

    def create(self, cat: CatCreate) -> CatResponse:
        try:
            with self._database.session() as session:
                repo = CatRepository(session)
                db_cat = repo.create(cat)
                return self._to_response(db_cat)
        except ForeignKeyError as e:
            raise OwnerNotFoundError(
                cat.owner_id,
                {"field": e.field, "error": str(e.original_error)}
            )
        except RecordNotFoundError as e:
            raise EntityNotFoundError(
                "Cat",
                0,
                {"original": str(e.original_error)}
            )
        except DatabaseOperationError as e:
            raise DomainError(
                "Не удалось создать кота",
                "CAT_CREATE_ERROR",
                {"error": str(e.original_error)}
            )

    def update(self, cat_id: int, cat: CatUpdate) -> Optional[CatResponse]:
        try:
            with self._database.session() as session:
                repo = CatRepository(session)
                db_cat = repo.update(cat_id, cat)
                return self._to_response(db_cat) if db_cat else None
        except RecordNotFoundError as e:
            raise EntityNotFoundError(
                "Cat",
                cat_id,
                {"original": str(e.original_error)}
            )
        except DatabaseOperationError as e:
            raise DomainError(
                f"Не удалось обновить кота {cat_id}",
                "CAT_UPDATE_ERROR",
                {"error": str(e.original_error)}
            )

    def delete(self, cat_id: int) -> bool:
        try:
            with self._database.session() as session:
                repo = CatRepository(session)
                return repo.delete(cat_id)
        except RecordNotFoundError as e:
            raise EntityNotFoundError(
                "Cat",
                cat_id,
                {"original": str(e.original_error)}
            )
        except DatabaseOperationError as e:
            raise DomainError(
                f"Не удалось удалить кота {cat_id}",
                "CAT_DELETE_ERROR",
                {"error": str(e.original_error)}
            )
