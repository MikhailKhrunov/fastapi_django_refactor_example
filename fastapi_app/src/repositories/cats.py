from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.cat_model import Cat as CatModel
from src.schemas.cats import CatCreate, CatUpdate, CatResponse


class CatRepository:
    """
    Репозиторий для одной таблицы.
    Принимает Pydantic-схемы, работает с SQLAlchemy.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CatModel]:
        return self.session.query(CatModel).offset(skip).limit(limit).all()

    def get_by_id(self, cat_id: int) -> Optional[CatModel]:
        return self.session.query(CatModel).filter(CatModel.id == cat_id).first()

    def get_by_owner(self, owner_id: int) -> List[CatModel]:
        return self.session.query(CatModel).filter(CatModel.owner_id == owner_id).all()

    def create(self, cat: CatCreate) -> CatModel:
        """Принимает Pydantic, возвращает SQLAlchemy"""
        from datetime import datetime

        age = datetime.now().year - cat.birth_year

        db_cat = CatModel(
            name=cat.name,
            color=cat.color,
            birth_year=cat.birth_year,
            owner_id=cat.owner_id,
            owner_username=f"user_{cat.owner_id}",
            owner_first_name=None,
            owner_last_name=None,
            age=age,
        )

        # Конвертируем достижения в JSON
        if cat.achievements:
            db_cat.set_achievements_list(cat.achievements)

        self.session.add(db_cat)
        return db_cat

    def update(self, cat_id: int, cat: CatUpdate) -> Optional[CatModel]:
        """Принимает Pydantic, возвращает SQLAlchemy"""
        db_cat = self.get_by_id(cat_id)
        if not db_cat:
            return None

        update_data = cat.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if value is not None:
                if field == "achievements":
                    db_cat.set_achievements_list(value)
                elif field == "birth_year":
                    from datetime import datetime

                    db_cat.age = datetime.now().year - value
                    setattr(db_cat, field, value)
                else:
                    setattr(db_cat, field, value)

        return db_cat

    def delete(self, cat_id: int) -> bool:
        db_cat = self.get_by_id(cat_id)
        if not db_cat:
            return False
        self.session.delete(db_cat)
        return True
