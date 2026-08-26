from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.piece_model import Piece, PieceUpdate
from database.piece_db import PieceDB




def get_all_pieces_repo(db :Session):
    return db.query(PieceDB).order_by(PieceDB.id).all()


def get_one_piece_by_id_repo(piece_id: int, db :Session):
    piece = db.query(PieceDB).filter(PieceDB.id == piece_id).first()
    if piece is None:
        raise HTTPException(status_code=404, detail="La piece recherchée n'existe pas")
    return piece


def create_piece_repo(piece_created : Piece, db :Session):
    piece_db = PieceDB(libelle_piece = piece_created.libelle_piece,
                       reference_piece = piece_created.reference_piece,
                       qte_stock_piece = piece_created.qte_stock_piece)

    db.add(piece_db)
    db.commit()
    db.refresh(piece_db)
    return piece_db


def update_piece_put_repo(piece_id : int, piece_updated : Piece, db : Session):
    piece = db.query(PieceDB).filter(PieceDB.id == piece_id).first()
    if piece is None:
        raise HTTPException(status_code=404, detail="La piece recherchée n'existe pas")

    piece.libelle_piece = piece_updated.libelle_piece
    piece.reference_piece = piece_updated.reference_piece
    piece.qte_stock_piece = piece_updated.qte_stock_piece
    db.commit()
    db.refresh(piece)
    return piece


def update_piece_patch_repo(piece_id : int, piece_updated : PieceUpdate, db : Session):
    piece = db.query(PieceDB).filter(PieceDB.id == piece_id).first()
    if piece is None:
        raise HTTPException(status_code=404, detail="La piece recherchée n'existe pas")

    updated_data = piece_updated.dict(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(piece, key, value)

    db.commit()
    db.refresh(piece)
    return piece


def delete_piece_by_id_repo (piece_id : int, db : Session):
    piece = db.query(PieceDB).filter(PieceDB.id == piece_id).first()
    if piece is None:
        raise HTTPException(status_code=404, detail="La piece recherchée n'existe pas")

    db.delete(piece)
    db.commit()
    return {"info": f"La piece {piece.libelle_piece} a bien ete supprimée"}


def get_critical_stock_pieces_repo(db: Session, seuil: int = 5):
    return db.query(PieceDB).filter(PieceDB.qte_stock_piece < seuil).order_by(PieceDB.qte_stock_piece).all()

    
    
    
