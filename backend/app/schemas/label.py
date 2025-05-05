from datetime import datetime

from pydantic import BaseModel, Field


class LabelBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    color: str = Field(pattern="^#[0-9A-Fa-f]{6}$")


class LabelCreate(LabelBase):
    pass


class LabelUpdate(LabelBase):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, pattern="^#[0-9A-Fa-f]{6}$")


class LabelResponse(LabelBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
