from database.user_db import UserDB
from models.user_model import User , UserUpdate, UserRole, UserOut
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.security import hash_password


def to_user_out(user_db: UserDB) -> UserOut:
    return UserOut(
        id=user_db.id,
        username=user_db.username,
        password=user_db.password,
        role=UserRole.ADMIN if user_db.is_admin else UserRole.USER
    )


def get_all_users_repo(db: Session):
    users = db.query(UserDB).order_by(UserDB.id).all()
    return [to_user_out(user) for user in users]


def get_one_user_repo(user_id : int, db: Session):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Le user recherché n'existe pas")
    return to_user_out(user)


def get_user_by_username_repo(username: str, db: Session):
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_user_by_username_for_dashboard_repo(username: str, db: Session):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    return to_user_out(user)


def create_user_repo(user_created: User, db: Session):
     user_db = UserDB(
          username=user_created.username,
          password=hash_password(user_created.password),
          is_admin=(user_created.role == UserRole.ADMIN))
     db.add(user_db)
     db.commit()
     db.refresh(user_db)
     return to_user_out(user_db)


def update_user_put_repo(user_id: int , updated_user: User, db: Session):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
             raise HTTPException(status_code=404, detail="User not found")

    user.username = updated_user.username
    user.password = hash_password(updated_user.password)
    user.role = updated_user.role

    db.commit()
    db.refresh(user)
    return to_user_out(user)


def update_user_patch_repo(user_id: int , user_updated : UserUpdate, db: Session):
    # récupération du UserDB avec l'id qui est egal a user_id passé en parametre 
    user_db = db.query(UserDB).filter(UserDB.id == user_id).first()
    # Test si le user existe bien en BDD
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Stockage des champs a modifier 
    update_data = user_updated.dict(exclude_unset=True)

    if "role" in update_data:
        role_value = update_data.pop("role")
        user_db.is_admin = (role_value == UserRole.ADMIN)

    if "password" in update_data:
        password_value = update_data.pop("password")
        user_db.password = hash_password(password_value)

    # Parcours de tous les champs de update_data 
    for key, value in update_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return to_user_out(user_db)


def delete_user_by_id_repo(user_id : int, db: Session):
    user_db = db.query(UserDB).filter(UserDB.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_db)
    db.commit()
    return {"info": f"le user {user_db.username} a bien ete supprimé"}