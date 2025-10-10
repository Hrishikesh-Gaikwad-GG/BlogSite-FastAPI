from fastapi import HTTPException, Query, APIRouter, status, Depends
from database import SessionDep
import schemas, models, utils
from sqlmodel import select
from routers import auth



router = APIRouter(
    prefix='/vote',
    tags = ['Vote']
)


@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, session : SessionDep,  user : models.User = Depends(auth.get_current_user)):


    # if post exists...
    post_exists = session.exec(select(models.Post).where(models.Post.id == vote.post_id)).first()
    if not post_exists:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Post with id {vote.post_id} does not exists.')
    
    # if user already voted...
    vote_query = select(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user.id)
    found_vote = session.exec(vote_query).first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'user {user.id} has already voted on post {vote.post_id}')
        
        new_vote = models.Votes(post_id = vote.post_id, user_id = user.id)
        session.add(new_vote)
        session.commit()
        return {"message": 'successfully added vote'}

    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'Vote does not exists')
        
        else:
            
            session.delete(found_vote)
            session.commit() 
            return {'message': 'successfully deleted vote'}



