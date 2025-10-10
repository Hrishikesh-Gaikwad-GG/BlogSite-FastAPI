from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal




class UserBase(BaseModel):
    email : EmailStr
    

class CreateUser(UserBase):
    password : str

class ResponseUser(UserBase):
    created_at : datetime
    id : int | None



class PostBase(BaseModel):
    title : str 
    content : str 
    published : bool 


class ResponsePost(PostBase):
    id: int 
    created_at : datetime
    owner_id : int
    owner : UserBase

class PostOut(BaseModel):
    Post : ResponsePost
    votes : int


class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    title : str | None = None
    content : str | None = None
    published : bool | None = None




class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    email : str |  None = None


class Vote(BaseModel):
    post_id : int
    dir : Literal[0, 1]