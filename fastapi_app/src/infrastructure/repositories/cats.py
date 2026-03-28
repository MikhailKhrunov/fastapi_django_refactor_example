from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from infrastructure.models.cat_model import Cat as CatModel
from schemas.cats import CatCreate, CatUpdate
# импорт через (), из-за flake8
from core.exceptions.database_exceptions import (
    DatabaseOperationError,
    RecordNotFoundError,
    ForeignKeyError,
)


class CatRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CatModel]:
        try:
            return self.session.query(CatModel).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationError("Ошибка получения списка котов", e)

    def get_by_id(self, cat_id: int) -> Optional[CatModel]:
        try:
            cat = self.session.query(CatModel).filter(
                CatModel.id == cat_id
            ).first()
            if not cat:
                raise RecordNotFoundError("Cat", cat_id)
            return cat
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationError(f"Ошибка получения кота {cat_id}", e)

    def create(self, cat: CatCreate) -> CatModel:
        try:
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

            if cat.achievements:
                db_cat.set_achievements_list(cat.achievements)

            self.session.add(db_cat)
            self.session.flush()
            return db_cat

        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in str(e):
                raise ForeignKeyError("owner_id", "User", cat.owner_id, e)
            raise DatabaseOperationError("Ошибка создания кота", e)
        except SQLAlchemyError as e:
            raise DatabaseOperationError("Ошибка создания кота", e)

    def update(self, cat_id: int, cat: CatUpdate) -> Optional[CatModel]:
        try:
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
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationError(f"Ошибка обновления кота {cat_id}", e)

    def delete(self, cat_id: int) -> bool:
        try:
            db_cat = self.get_by_id(cat_id)
            if not db_cat:
                return False
            self.session.delete(db_cat)
            return True
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationError(f"Ошибка удаления кота {cat_id}", e)
