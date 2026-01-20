# import sys
# print(sys.path)
from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent.parent
# sys.path.insert(0,str(ROOT_PATH))
# print(sys.path)
from fastapi import FastAPI
# from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from routers import post, user, auth, vote


app = FastAPI()


# @app.on_event('startup')
# def on_startup():
#     create_db_and_tables()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'Hello Space'}