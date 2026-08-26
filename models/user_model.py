from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional
from enum import Enum


def check_length(value: str):
    if not value:
        raise ValueError("Champ obligatoire")

    if len(value) < 3:
        raise ValueError("Doit contenir au moins 3 caractères")

    return value


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"    

# modele de base pour toutes les methodes sauf la methode PATCH
class User(BaseModel):
    username: Annotated[str, AfterValidator(check_length)]
    password: Annotated[str, AfterValidator(check_length)]
    role: UserRole = UserRole.USER

# modele uniquement pour la methode PATCH
# Les attributs sont optionnels pour eviter de faire comme pour un PUT
class UserUpdate(BaseModel):
    username: Annotated[Optional[str], AfterValidator(check_length)] = None
    password: Annotated[Optional[str], AfterValidator(check_length)] = None
    role: Optional[UserRole] = None

# Cette classe permet d'afficher les champs dans un ordre bien précis 
class UserOut(BaseModel):
    id: int
    username: str
    password: str
    role : UserRole

    class Config:
        from_attributes = True
