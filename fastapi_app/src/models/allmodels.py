from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import datetime as dt

class MyColors(str, Enum):
    GREY = "Grey"
    BLACK = "Black"
    WHITE = "White"
    GINGER = "Ginger"
    MIXED = "Mixed"

class User(BaseModel):
    id: Optional[int] = None
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class Achievement(BaseModel):
    id: Optional[int] = None
    name: str

class AchievementCat(BaseModel):
    id: Optional[int] = None
    achievement: Achievement
    cat_id: int

class Cat(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=16)
    color: MyColors
    birth_year: int
    owner: User
    achievements: List[Achievement] = []