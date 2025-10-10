from fastapi import HTTPException, Query, APIRouter
from database import SessionDep
import schemas, models, utils

router = APIRouter(
    prefix= "/users",
    tags = ["User"]
)


@router.post("/", status_code = 201, response_model = schemas.ResponseUser)
def create_user(user : schemas.CreateUser, session : SessionDep):
    user_data = models.User.model_validate(user)
    hashed_password = utils.get_password_hash(user_data.password)
    user_data.password = hashed_password
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@router.get("/{id}", response_model = schemas.ResponseUser)
def get_user(id: int, session : SessionDep):
    user = session.get(models.User, id)
    if not user:
        raise HTTPException(status_code= 404, detail = "User not found")
    return user  