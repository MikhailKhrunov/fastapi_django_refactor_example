from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.models.user_model import User as UserModel
from core.security import hash_password, verify_password


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.username == username).first()

    def create(self, username: str, password: str, first_name: str = None, last_name: str = None) -> UserModel:
        db_user = UserModel(
            username=username,
            password=hash_password(password),
            first_name=first_name,
            last_name=last_name,
        )
        self.session.add(db_user)
        self.session.flush()
        return db_user

    def verify_password(self, user: UserModel, password: str) -> bool:
        return verify_password(password, user.password)
