from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional

def check_piece_info(value: Optional[str]):
    if value is None:
        return value
    if not value.strip():
        raise ValueError("Libelle/Reference : obligatoire")
    return value.strip()

    
def check_piece_stock(value : int):
    if not value:
        raise ValueError("La quantité est obligatoire")

    if value < 0:
        raise ValueError("la quantité de pieces doit etre positive")
    
    return value





class Piece(BaseModel):   
    libelle_piece: Annotated[str, AfterValidator(check_piece_info)]
    reference_piece: Annotated[str, AfterValidator(check_piece_info)]
    qte_stock_piece : Annotated[int, AfterValidator(check_piece_stock)]

class PieceUpdate(BaseModel):
    libelle_piece: Annotated[Optional[str], AfterValidator(check_piece_info)] = None
    reference_piece: Annotated[Optional[str], AfterValidator(check_piece_info)] = None
    qte_stock_piece : Annotated[Optional[int], AfterValidator(check_piece_stock)] = None


class PieceOut(BaseModel):
    id: int
    libelle_piece: str
    reference_piece: str
    qte_stock_piece: int

    class Config:
        from_attributes = True