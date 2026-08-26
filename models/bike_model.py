from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional

# Methodes de verification 
def check_bike_number(value: str):
    if not value:
        raise ValueError("Numéro de vélo obligatoire")

    value = value.strip()

    if len(value) < 2:
        raise ValueError("Numéro de vélo trop court")

    if len(value) > 4:
            raise ValueError("Numéro de vélo trop long")

    return value


def check_longueur_attribution(value: str):
        if value is None:
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError("La valeur ajoutée a nom ou prénom est trop courte")
        return value


# constructeurs des modeles
class Bike (BaseModel):
    bike_number: Annotated[str, AfterValidator(check_bike_number)]
    attribution_nom : Annotated[Optional[str], AfterValidator(check_longueur_attribution)] = None
    attribution_prenom :Annotated[Optional[str], AfterValidator(check_longueur_attribution)] = None


class BikeUpdate(BaseModel):
    bike_number: Annotated[Optional[str], AfterValidator(check_bike_number)] = None
    attribution_nom : Annotated[Optional[str], AfterValidator(check_longueur_attribution)] = None
    attribution_prenom :Annotated[Optional[str], AfterValidator(check_longueur_attribution)] = None


# Cette classe permet d'afficher les champs dans un ordre bien précis 
class BikeOut(BaseModel):
    id: int
    bike_number: str
    attribution_nom: Optional[str] = None
    attribution_prenom: Optional[str] = None

    class Config:
        from_attributes = True