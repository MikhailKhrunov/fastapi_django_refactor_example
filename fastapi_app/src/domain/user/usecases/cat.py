from typing import List, Optional

from database import database
from repositories.cats import CatRepository
from schemas.cats import CatCreate, CatUpdate, CatResponse
from models.cat_model import Cat as CatModel


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
        with self._database.session() as session:
            repo = CatRepository(session)
            cats = repo.get_all(skip=skip, limit=limit)
            return [self._to_response(cat) for cat in cats]

    def get_by_id(self, cat_id: int) -> Optional[CatResponse]:
        with self._database.session() as session:
            repo = CatRepository(session)
            cat = repo.get_by_id(cat_id)
            return self._to_response(cat) if cat else None

    def create(self, cat: CatCreate) -> CatResponse:
        with self._database.session() as session:
            repo = CatRepository(session)
            db_cat = repo.create(cat)
            return self._to_response(db_cat)

    def update(self, cat_id: int, cat: CatUpdate) -> Optional[CatResponse]:
        with self._database.session() as session:
            repo = CatRepository(session)
            db_cat = repo.update(cat_id, cat)
            return self._to_response(db_cat) if db_cat else None

    def delete(self, cat_id: int) -> bool:
        with self._database.session() as session:
            repo = CatRepository(session)
            return repo.delete(cat_id)
