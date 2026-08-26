from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional
from enum import Enum
from models.piece_model import PieceOut
from datetime import datetime
from models.bike_model import BikeOut
from models.user_model import UserOut


def check_user_bike_exsit(value: int):
    if not value:
        raise ValueError("L'utilisateur ou le velo sont obligatoires")
    return value

def check_date_exist(value : datetime):
     if not value:
          raise ValueError("La date est obligatoire")
     return value


# classe pour pouvoir créer des objets RepairPieceInput
# Permettra de savoir quelles pieces ont été changées et combien d'entre-elles
class RepairPieceInput(BaseModel):
    piece_id: int
    quantite: int = 1

# classe pour pouvoir créer des objets RepairPieceOut
# Permettra l'affichage des pieces qui ont été changées et combien d'entre-elles
class RepairPieceOut(BaseModel):
    piece: PieceOut
    quantite: int

    class Config:
        from_attributes = True


class RepairStatus(str, Enum):
    A_FAIRE = "a_faire"
    TERMINE = "termine"    
    SUSPENDU = "suspendu"




class Repair(BaseModel):
    bike_id: Annotated[int, AfterValidator(check_user_bike_exsit)]
    user_id: Optional[str] = None
    date_reparation : Optional[datetime] = None
    commentaire : Optional[str] = None
    statut: RepairStatus = RepairStatus.A_FAIRE
    pieces : Optional[list[RepairPieceInput]] = None


class RepairUpdate(BaseModel):
    bike_id : Optional[int] = None
    user_id : Optional[int] = None
    date_reparation : Optional[datetime] = None
    commentaire : Optional[str] = None
    statut : Optional[RepairStatus] = None
    pieces : Optional[list[RepairPieceInput]] =  None 


class RepairOut(BaseModel):
    id: int
    bike: BikeOut
    user: UserOut
    date_reparation: datetime
    commentaire: Optional[str] = None
    statut: RepairStatus
    pieces: Optional[list[RepairPieceOut]] = None

    class Config:
        from_attributes = True