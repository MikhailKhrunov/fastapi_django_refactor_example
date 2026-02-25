from pydantic import BaseModel, Field, ConfigDict
from src.schemas.achievements import AchievementBase
from typing import Literal, List, Optional

MyColors = Literal["Grey", "Black", "White", "Ginger", "Mixed"]

class BaseCat(BaseModel):
    name: str = Field(..., min_length=1, max_legnth=16)
    color: MyColors
    birth_year: int = Field(..., gr=1900, le=2100) # ge - >=, le - <=

class CatCreate(BaseCat):
    owner_id: int
    achievements: Optional[List[str]] = Field(default_factory=list)

class CatUpdate(BaseCat):
    color: Optional[MyColors] = None
    achievements: Optional[List[str]] = None

class CatResponse(BaseCat):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    achievements: List[str] = Field(default_factory=list)
    age: int
