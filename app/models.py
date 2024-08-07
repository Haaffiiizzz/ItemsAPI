from .database import Base
from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, text

class Country(Base):
    __tablename__ = "Countries_Private"
    country = Column(String, primary_key=True, unique=True)
    items = Column(JSON)

class Country2(Base):
    __tablename__ = "Countries_Public"
    country = Column(String, primary_key=True, unique=True)
    items = Column(JSON)


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key= True, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, 
                       server_default= text('now()'))

# here we create the model for the countries and users table to be used with the db query
