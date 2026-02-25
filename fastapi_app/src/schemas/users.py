from pydantic import BaseModel, SecretStr, Field, ConfigDict
from typing import Optional


class User(BaseModel):
    login: str
    password: SecretStr

class BaseUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(BaseUser):
    pass

class UserUpdate(BaseUser):
    pass

class UserResponse(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: int
