from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, List, Optional

MyColors = Literal["Gray", "Black", "White", "Ginger", "Mixed"]


class BaseCat(BaseModel):
    name: str = Field(..., min_length=1, max_length=16)
    color: MyColors
    birth_year: int = Field(..., ge=1900, le=2100)  # ge - >=, le - <=


class CatCreate(BaseCat):
    owner_id: int
    achievements: Optional[List[str]] = Field(default_factory=list)


class CatUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=16)
    color: Optional[MyColors] = None
    birth_year: Optional[int] = Field(None, ge=1900, le=2100)
    achievements: Optional[List[str]] = None


class CatResponse(BaseCat):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    achievements: List[str] = Field(default_factory=list)
    age: int
