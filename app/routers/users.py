from fastapi import status, HTTPException, Depends, APIRouter
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
import schemas
import models
from utils import hashPassword
import oauth2


router = APIRouter(prefix = "/users", tags = ['Users'])

metadata = MetaData()
countriesTable = Table('Countries1', metadata, autoload_with=engine)

models.Base.metadata.create_all(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def Create_User(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # hash the password then add the edited input (user) to the database
    hashedPassword = hashPassword(user.password)
    user.password = hashedPassword
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def Get_User(id: int, db: Session = Depends(get_db), currUser: int = Depends(oauth2.getCurrentUser)):
    # get a particular user's info
    # with depends, code doesnt run unless it happens
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user