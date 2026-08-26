from sqlalchemy.orm import Session
import repositories.piece_repository as piece_repository
from models.piece_model import Piece, PieceUpdate, PieceOut

def get_all_pieces_services(db : Session):
    return piece_repository.get_all_pieces_repo(db)


def get_one_piece_by_id_services(piece_id : int , db : Session):
    return piece_repository.get_one_piece_by_id_repo(piece_id, db)


def create_piece_service(piece : Piece, db: Session):
    return piece_repository.create_piece_repo(piece ,db)


def update_piece_put_service(piece_id :int ,piece : Piece, db : Session):
    return piece_repository.update_piece_put_repo(piece_id, piece, db)


def update_piece_patch_service(piece_id :int ,piece : PieceUpdate, db : Session):
    return piece_repository.update_piece_patch_repo(piece_id, piece, db)


def delete_piece_by_id_service(piece_id : int , db : Session):
    return piece_repository.delete_piece_by_id_repo(piece_id ,db)



# Pour la page d'onboarding 
def get_critical_stock_service(db : Session):
    return piece_repository.get_critical_stock_pieces_repo(db)