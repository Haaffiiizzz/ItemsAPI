from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key= True, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, 
                       server_default= text('now()'))

# here we create the model for the users table to be used with the db query
# theres none for country here because i already created country table and 
# cant manually put in all the fields. thats also why i didnt use sqlalchemy 
# for adding to countries