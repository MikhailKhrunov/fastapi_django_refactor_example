from sqlalchemy import Column, Integer, String
import json

from src.database import Base


class Cat(Base):
    """Одна модель со всеми полями в одной таблице"""
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False)
    color = Column(String(16), nullable=False)
    birth_year = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    owner_username = Column(String(150), nullable=False)
    owner_first_name = Column(String(150), nullable=True)
    owner_last_name = Column(String(150), nullable=True)
    achievements = Column(String, default="[]")  # JSON как текст
    age = Column(Integer, nullable=False)

    # JSON поле achievements
    def get_achievements_list(self) -> list[str]:
        """Получить достижения как список"""
        try:
            return json.loads(self.achievements) if self.achievements else []
        except (json.JSONDecodeError, TypeError):
            return []

    def set_achievements_list(self, achievements: list[str]):
        """Установить достижения из списка"""
        import json
        self.achievements = json.dumps(achievements, ensure_ascii=False)
