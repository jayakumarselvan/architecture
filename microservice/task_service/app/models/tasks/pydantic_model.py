import datetime

from pydantic import BaseModel, Field
from typing import Literal, Optional


class TaskCreateUpdateRequest(BaseModel):
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Description of the project")
    dueDate: datetime.datetime = Field(..., description="Due datetime")
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    status: Literal["TODO", "IN PROGRESS", "DONE"]
    assignedUserId: str = Field(..., description="User id of assignee")


class TaskPatchUpdateRequest(BaseModel):
    priority: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = None
    status: Optional[Literal["TODO", "IN PROGRESS", "DONE"]] = None
    assignedUserId: Optional[str] = Field(None, description="User ID of the assignee")
