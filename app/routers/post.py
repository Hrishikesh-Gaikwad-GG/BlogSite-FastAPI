from fastapi import FastAPI, Response, status, HTTPException, Query, APIRouter, Depends

from fastapi.responses import JSONResponse

from typing import Annotated, List, Optional
from sqlmodel import select, func
import schemas, models, utils
from database import SessionDep

from routers import auth



router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)




# @router.get('/', response_model = List[schemas.ResponsePost], status_code= 200)
@router.get('/', response_model = List[schemas.PostOut], status_code = 200)
def get_posts(
    session : SessionDep,
    offset : int = 0,
    limit : Annotated[int, Query(le = 10)] = 10,
    search : Optional[str] = '',
    user_id : int = Depends(auth.get_current_user)

):
    
    # posts = session.exec(select(models.Post).filter(models.Post.title.contains(search)).offset(offset).limit(limit)).all()

    result = session.exec(select(models.Post, func.count(models.Votes.post_id).label('votes'))\
                          .join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True)\
                            .group_by(models.Post.id)\
                                .filter(models.Post.title.contains(search)).offset(offset).limit(limit)).all()

    return result

@router.get("/me", response_model = List[schemas.ResponsePost])
def get_my_posts(
    session : SessionDep,
    offset : int = 0,
    limit : Annotated[int, Query(le = 10)] = 10,
    user : models.User = Depends(auth.get_current_user)
):
    statement = select(models.Post).where(models.Post.owner_id == user.id).offset(offset).limit(limit)
    posts = session.exec(statement).all()
    return posts

@router.post("/", response_model = schemas.ResponsePost, status_code=201)
def create_posts(data : schemas.CreatePost, session : SessionDep, user = Depends(auth.get_current_user)):

    data = data.model_dump()
    data.update(owner_id = user.id)
    post_db = models.Post.model_validate(data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db

@router.get("/{id}", response_model = List[schemas.PostOut], status_code=200)
def get_post(id : int, session: SessionDep, user_id : int = Depends(auth.get_current_user)):
    # post = session.get(models.Post,id)

    statement = select(models.Post, func.count(models.Votes.post_id).label('votes'))\
                          .join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True)\
                            .group_by(models.Post.id).filter(models.Post.id == id)
    
    post = session.exec(statement).all()
    
    if not post:
        raise HTTPException(status_code= 404, detail= "Post not found")
    return post

@router.patch("/{id}", response_model = schemas.ResponsePost, status_code = 200)
def update_post(id : int, data : schemas.UpdatePost, session : SessionDep, user : models.User = Depends(auth.get_current_user)):

    db_post = session.get(models.Post, id)
    if not db_post:
        raise HTTPException(status_code=404, detail= "Post not found")
    
    if db_post.owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the requested action")

    updated_post = data.model_dump(exclude_unset = True)

    db_post.sqlmodel_update(updated_post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.delete("/{id}", status_code= 200)
def delete_post(id: int, session: SessionDep, user : models.User = Depends(auth.get_current_user)):


    post = session.get(models.Post, id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Post not found")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the requested action") 

    session.delete(post)
    session.commit()
    return JSONResponse({"message": "Post Deleted"}, status_code = 200)