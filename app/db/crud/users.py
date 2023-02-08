from sqlalchemy.orm import Session
from db.schemas import users as users_schemas
from db.models import users as users_model
from utils import hashpw, checkpw

#유저 신규 생성
def create_user(db: Session, user:users_schemas.UserCreate):    
    new_user = users_model.Users(user_email=user.user_email, user_password=user.user_password, auth_yn=False)
    
    if get_user_by_email(db, user.user_email) is not None:
        print("Already Existing email")
        return None
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#유저 이메일로 유저 단건 조회
def get_user_by_email(db: Session, email: str):
    return db.query(users_model.Users)\
             .filter(users_model.Users.user_email == email).first()

#유저 패스워드 변경
def update_passwd(db: Session, db_user, new_password):
    db_user.user_password = hashpw(new_password)
    db.commit()

#유저 정보 삭제
def delete_user_by_email(db:Session, db_user):
    db.delete(db_user)
    db.commit()