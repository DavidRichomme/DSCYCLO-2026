from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database.database import get_db
from models.piece_model import Piece, PieceUpdate, PieceOut
import services.piece_services as piece_services
# pour les logs 
from utils.auth import get_current_user
import services.activity_log_service as activity_log_services
from models.activity_log_model import ActivityLog, ActionType

router = APIRouter(tags=["Pièces"])

@router.get("/pieces/" ,response_model=list[PieceOut])
def get_pieces_list_route( db: Session =Depends(get_db)):
    return piece_services.get_all_pieces_services(db)


@router.get("/pieces/{piece_id}", response_model=PieceOut)
def get_piece_by_id_route( piece_id :int , db : Session = Depends(get_db)):
    return piece_services.get_one_piece_by_id_services(piece_id ,db)


@router.post("/pieces/", response_model=PieceOut)
def create_piece_route( piece : Piece , db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = piece_services.create_piece_service(piece ,db)
    log = ActivityLog(username=current_user.username, action=ActionType.CREATE, objet="piece")
    activity_log_services.create_activity_log_service(log, db)
    return result


@router.put("/pieces/{piece_id}", response_model=PieceOut)
def update_piece_put_route(piece_id : int, piece : Piece, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = piece_services.update_piece_put_service(piece_id, piece, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="piece")
    activity_log_services.create_activity_log_service(log, db)
    return result


@router.patch("/pieces/{piece_id}", response_model=PieceOut)
def update_piece_patch_route(piece_id : int, piece : PieceUpdate, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = piece_services.update_piece_patch_service(piece_id, piece, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="piece")
    activity_log_services.create_activity_log_service(log, db)
    return result


@router.delete("/pieces/{piece_id}")
def delete_piece_by_id_route(piece_id : int , db :Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = piece_services.delete_piece_by_id_service(piece_id, db)
    log = ActivityLog(username=current_user.username, action=ActionType.DELETE, objet="piece")
    activity_log_services.create_activity_log_service(log, db)
    return result