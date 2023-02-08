from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from db.connection import get_db
from db.service import image_bundle as image_bundle_service
from typing import List
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/image_bundle", # url 앞에 고정적으로 붙는 경로추가
)

templates = Jinja2Templates(directory='templates')


@router.post("/upload_images")
def upload_images(request: Request
                , access_auth : str = Form(...)
                , db: Session = Depends(get_db)
                , images: List[UploadFile] = File(...)
                , user_email: str = Form(...)) :
    
    access_auth = True if access_auth =="yes" else False
    
    paths, image_bundle_id = image_bundle_service.upload_images(db, user_email, images)
    context = {
        'request': request,
        'paths': paths,
        'image_bundle_id':image_bundle_id
    }
    return templates.TemplateResponse('loading.html', context=context)