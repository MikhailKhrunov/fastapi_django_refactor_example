from pydantic import BaseModel, Field, ConfigDict


class BaseAchievement(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)


class AchievementCreate(BaseAchievement):
    pass


class AchievementResponse(BaseAchievement):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    achievement_name: str = Field(..., alias="name")
