from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ActionType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"


class ActivityLog(BaseModel):
    username: str
    action: ActionType
    objet: str


class ActivityLogOut(BaseModel):
    id: int
    username: str
    action: ActionType
    objet: str
    date_action: datetime

    class Config:
        from_attributes = True