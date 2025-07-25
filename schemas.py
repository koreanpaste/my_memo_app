from pydantic import BaseModel
from typing import Optional 

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str
class MemoCreate(BaseModel):
    title:Optional[str] = None
    content:Optional[str] = None

class MemoUpdate(BaseModel):
    title:Optional[str] =None
    contnet:Optional[str] =None