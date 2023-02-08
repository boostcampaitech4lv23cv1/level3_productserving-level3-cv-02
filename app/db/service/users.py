from db.crud import users
from utils import hashpw, checkpw

def create_user(db, user):
    user.user_password = hashpw(user.user_password)
    
    return users.create_user(db, user)

def get_user_by_email(db, email):
    return users.get_user_by_email(db, email)

def update_passwd(db, user):
    db_user = get_user_by_email(db, user.user_email)
    if checkpw(user.user_password, db_user.user_password) == False:
        raise Exception('비밀번호가 다릅니다.')
    users.update_passwd(db, db_user, user.new_password)

def delete_user_by_email(db, user):
    db_user = get_user_by_email(db, user.user_email)
    if checkpw(user.user_password, db_user.user_password) == False:
        raise Exception('비밀번호가 다릅니다.')

    users.delete_user_by_email(db, db_user)

def checkpassword(db, email, pw):
    db_user = get_user_by_email(db, email)
    if db_user is None:
        return False
    return checkpw(pw, db_user.user_password)