from sqlmodel import Field, SQLModel, text, Relationship
from datetime import datetime
# from sqlalchemy.orm import relationship
# import schemas
from typing import Optional, List







class Post(SQLModel , table = True):

    __tablename__ = 'posts'
    id: int | None = Field(None, primary_key= True, nullable= False)
    title : str = Field(index = True, nullable= False)
    content : str = Field(nullable= False)
    published : bool | None = Field(None, nullable= False, sa_column_kwargs= {"server_default": text("TRUE")})
    created_at : datetime = Field(default_factory = datetime.now ,
                                  nullable = False,
                                  sa_column_kwargs={'server_default': text('now()')})

    owner_id : int = Field(foreign_key = "users.id", ondelete = "CASCADE", nullable = False)

    owner : Optional["User"] = Relationship(back_populates="posts")


class User(SQLModel, table = True):
    __tablename__ = "users"
    id : int | None = Field(None, primary_key = True, nullable = False)
    email : str = Field(nullable = False, unique = True)
    password : str = Field(nullable = False)
    created_at : datetime = Field(default_factory = datetime.now,
                                   nullable = False,
                                   sa_column_kwargs={'server_default': text("now()")})
    
    posts : List["Post"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"})



class Votes(SQLModel, table = True):
    __tablename__ = 'votes'
    user_id : int = Field(foreign_key='users.id', ondelete= 'CASCADE' , primary_key= True)

    post_id : int = Field(foreign_key='posts.id', ondelete= 'CASCADE' , primary_key= True)


metadata = SQLModel.metadata
    
# class User(SQLModel, table = True):
#     __tablename__ = "users"
#     # id : int | None = Field(None, nullable = False, unique = True, sa_column_kwargs={'server_defalut': text("nextval('nextval('users_id_seq'::regclass)")})
#     email : str = Field(nullable = False, primary_key = True)
#     password : str = Field(nullable = False)
#     created_at : datetime = Field(default_factory = datetime.now,
#                                    nullable = False,
#                                    sa_column_kwargs={'server_default': text("now()")})

