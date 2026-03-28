from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Literal, List, Optional
from datetime import datetime


MyColors = Literal["Gray", "Black", "White", "Ginger", "Mixed"]


class BaseCat(BaseModel):
    name: str = Field(..., min_length=1, max_length=16)
    color: MyColors
    birth_year: int = Field(..., ge=1900, le=2100)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Имя не может быть пустым')
        if not v[0].isalpha():
            raise ValueError('Имя должно начинаться с буквы')
        return v.strip()

    @field_validator('birth_year')
    @classmethod
    def validate_birth_year(cls, v: int) -> int:
        if v > datetime.now().year:
            raise ValueError(f'Год не может быть больше {datetime.now().year}')
        return v


class CatCreate(BaseCat):
    owner_id: int
    achievements: Optional[List[str]] = Field(default_factory=list)

    @field_validator('owner_id')
    @classmethod
    def validate_owner_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID владельца должен быть положительным')
        return v

    @field_validator('achievements')
    @classmethod
    def validate_achievements(
        cls,
        v: Optional[List[str]]
    ) -> Optional[List[str]]:
        if v is None:
            return []
        for ach in v:
            if not ach.strip() or len(ach) > 64:
                raise ValueError('Некорректное достижение')
        return v


class CatUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=16)
    color: Optional[MyColors] = None
    birth_year: Optional[int] = Field(None, ge=1900, le=2100)
    achievements: Optional[List[str]] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip() or not v[0].isalpha():
                raise ValueError('Некорректное имя')
            return v.strip()
        return v

    @field_validator('birth_year')
    @classmethod
    def validate_birth_year(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v > datetime.now().year:
            raise ValueError(f'Год не может быть больше {datetime.now().year}')
        return v


class CatResponse(BaseCat):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    achievements: List[str] = Field(default_factory=list)
    age: int
