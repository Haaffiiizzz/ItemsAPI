from fastapi import status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from ..schemas import UserResponse, CreateUser
from ..models import Base, User
from ..utils import hashPassword
from ..oauth2 import getCurrentUser


router = APIRouter(prefix = "/users", tags = ['Users'])


Base.metadata.create_all(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def Create_User(user: CreateUser, db: Session = Depends(get_db)):
    # hash the password then add the edited input (user) to the database
    hashedPassword = hashPassword(user.password)
    user.password = hashedPassword
    newUser = User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def Get_User(id: int, db: Session = Depends(get_db), currUser: int = Depends(getCurrentUser)):
    # get a particular user's info
    # with depends, code doesnt run unless it happens
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user