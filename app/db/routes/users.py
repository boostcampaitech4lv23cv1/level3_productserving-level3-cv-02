from fastapi import APIRouter, Depends, Form, Body, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.connection import get_db
from db.service import users as users_service
from db.schemas import users as users_schema
from typing import Any
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from utils import send_email, send_mp3_email


router = APIRouter(
    prefix="/users", # url 앞에 고정적으로 붙는 경로추가
)


templates = Jinja2Templates(directory='templates')


'''
유저 신규 생성
이메일, 패스워드 필요
생성 후 인증메일 발송
'''
def create_user(db: Session = Depends(get_db), user:users_schema.UserCreate=None):
    res = users_service.create_user(db, user)
    return {"res": res}


# (TODO) 한번에 받아오는 방법을 찾아보자!
@router.post("/sign-check")
def create_user(request: Request, db: Session = Depends(get_db), user_email : str= Form(...), user_password: str = Form(...)):
    user_email = str(user_email)
    user_password = str(user_password)
    user = users_schema.UserCreate(user_email = user_email , user_password = user_password)
    res = users_service.create_user(db, user)
    
    if res is None:
        print("Already registered")
        return templates.TemplateResponse('error.html', context = {"request" : request})
    
    auth_num = send_email(user_email)
    
    
    # print("MP3 전송중!")
    # send_mp3_email(user_email
    #                ,"/opt/ml/xml/bC7YczPIJWON292a/0_ori_ring_teaser.png"
    #                , "/opt/ml/sound/bC7YczPIJWON292a/result_0.mp3"
    #                )
    
    print("Email 전송 완료")    
    return templates.TemplateResponse('sign-check.html', context={'request': request, "auth_num" : auth_num})


'''
유저 이메일로 유저 단건 조회
이메일 필요
'''
#(TODO) 원래는 인증여부도 확인해야할 것 같음
@router.get("/index")
def get_user_by_email(db: Session = Depends(get_db), email='unkwon@unkwon.com'):
    res = users_service.get_user_by_email(db, email)
    return {"res": res}

'''
유저 패스워드 변경
이메일, 패스워드, 새 패스워드 필요.
기존 패스워드 틀릴 시 error 발생.
'''
@router.put("/index")
def update_passwd(db: Session = Depends(get_db), user:users_schema.UserPasswdUpdate=None):
    users_service.update_passwd(db, user)


'''
유저 삭제
이메일, 패스워드 필요.
패스워드 틀릴 시 error 발생
'''
@router.delete("/index")
def delete_user_by_email(db: Session = Depends(get_db), user:users_schema.UserDelete=None):
    users_service.delete_user_by_email(db, user)


'''
비밀번호 체크
'''
@router.post("/checkpw")
def checkpassword(db: Session = Depends(get_db), user_email = "unkwon@unkwon.com", user_password=""):
    return users_service.checkpassword(db, user_email, user_password)