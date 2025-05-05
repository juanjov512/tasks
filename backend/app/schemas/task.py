from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=1000)
    due_date: datetime | None = None
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")
    priority: str | None = Field(None, pattern="^(low|medium|high)$")
    category_id: int | None = None
    labels: list[int] | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=1000)
    due_date: datetime | None = None
    status: str | None = Field(None, pattern="^(pending|in_progress|completed)$")
    priority: str | None = Field(None, pattern="^(low|medium|high)$")
    category_id: int | None = None
    labels: list[int] | None = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
