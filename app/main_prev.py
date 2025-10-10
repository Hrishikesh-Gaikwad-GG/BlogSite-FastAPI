from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from fastapi.params import Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Annotated
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlmodel import Session, SQLModel, select
from models import Post, User
from schemas import ResponsePost, CreatePost, UpdatePost, CreateUser, ResponseUser
from database import create_db_and_tables, SessionDep
import utils



app = FastAPI()


@app.on_event('startup')
def on_startup():
    create_db_and_tables()



@app.get('/')
def root():
    return {'message': 'Hello Space'}

@app.get('/posts', response_model = list[ResponsePost], status_code= 200)
def get_posts(
    session : SessionDep,
    offset : int = 0,
    limit : Annotated[int, Query(le = 10)] = 10
):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts

    

@app.post("/posts", response_model = ResponsePost, status_code=201)
def create_posts(data : CreatePost, session : SessionDep):
    post_db = Post.model_validate(data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db

@app.get("/posts/{id}", response_model = ResponsePost, status_code=200)
def get_post(id : int, session: SessionDep):
    post = session.get(Post ,id)
    if not post:
        raise HTTPException(status_code= 404, detail= "Post not found")
    return post

@app.patch("/posts/{id}", response_model = ResponsePost, status_code = 200)
def update_some(id : int, data : UpdatePost, session : SessionDep):

    db_post = session.get(Post, id)
    if not db_post:
        raise HTTPException(status_code=404, detail= "Post not found")

    updated_post = data.model_dump(exclude_unset = True)

    db_post.sqlmodel_update(updated_post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.delete("/posts/{id}", status_code= 200)
def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail= "Post not found")
    session.delete(post)
    session.commit()
    return JSONResponse({"message": "Post Deleted"}, status_code = 200)


@app.post("/users", status_code = 201, response_model = ResponseUser)
def create_user(user : CreateUser, session : SessionDep):
    user_data = User.model_validate(user)
    hashed_password = utils.get_password_hash(user_data.password)
    user_data.password = hashed_password
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@app.get("/user/{id}", response_model = ResponseUser)
def get_user(id: int, session : SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code= 404, detail = "User not found")
    return user
    # session.get_one()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user = 'postgres',password = 'root', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connection to database failed !")
#         print("ERROR: ", error)
#         time.sleep(3)

# my_posts = [
#     {"title": "title of Post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I like pizza", "id": 2}
# ]

# def find_post(id):
#     for d in my_posts:
#         if d['id'] == id:
#             return my_posts.index(d)



# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     # post_dict = post.model_dump()
#     # title = post_dict['title']
#     # content = post_dict['content']
#     # published = post_dict['published']
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
    
#     return {"data": new_post}



# @app.get("/posts/{id}")
# def get_post(id : int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with id: {id} was not found !"}
#     return {"data": post}


# @app.get("/posts/{id}")
# def get_post(id : int):
#     # post_id = find_post(id)
#     # if type(post_id) != int:
#     #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#     #                         detail= f"post with id: {id} was not found !")
#     # post = my_posts[post_id]

#     cursor.execute("""SELECT * FROM posts WHERE id = (%s)""",(id,))
#     post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail= f"post with id: {id} was not found !")
    # return {"data": post}


# @app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # post_id = find_post(id)
#     # if type(post_id) != int:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found !")
#     # my_posts.pop(post_id)
#     cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""",(id,))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail= f"post with id: {id} was not found !")
#     return Response(status_code= status.HTTP_204_NO_CONTENT)



# @app.put("/posts/{id}")
# def update_post(id: int, post : Post):
    
#     # post_id = find_post(id)
#     # if post_id == None:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found !")
#     # updated_dict = post.model_dump()
#     # updated_dict['id'] = id
#     # my_posts[post_id] = updated_dict
#     cursor.execute("""UPDATE posts SET title = (%s), content = (%s), published = (%s) WHERE id = (%s) RETURNING *""",(post.title, post.content, post.published, id))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail= f"post with id: {id} was not found !")

#     return {"udated_post": updated_post}