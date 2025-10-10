from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from typing import Annotated
from config import settings



# DATABASE_URL = f'postgresql://postgres:root@localhost/fastapi'
DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}\
@{settings.database_hostname}:5432/{settings.database_name}'

engine = create_engine(DATABASE_URL)



# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]




