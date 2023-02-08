from typing import Optional, List
from pydantic import BaseModel

class UserBase(BaseModel):
    user_email: str    
class Users(UserBase):
    user_id: int
    user_password: str
    auth_yn: bool
    image_bundle: List



class UserCreate(UserBase):
    user_password: str

class UserPasswdUpdate(UserBase):
    user_password: str
    new_password: str

class UserDelete(UserBase):
    user_password: str
