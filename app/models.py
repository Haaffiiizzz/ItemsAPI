from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

class Country(Base):
    __tablename__ = "Countries1"
    name = Column(String, unique = True, primary_key=True)
    Coke_0_33_Liter = Column(Integer)
    Gasoline_Petrol_1_Liter = Column(Integer)
    Eggs_1_Dozen = Column(Integer)
    Beef_1_KG = Column(Integer)
    Rice_1_KG = Column(Integer)
    Apples_1_KG = Column(Integer)
    Loaf_of_Bread_500g = Column(Integer)
    Water_1_5_Liters = Column(Integer)
    Toyota_Corolla = Column(Integer)
    Milk_1_Liter = Column(Integer)
    Hair_Cut = Column(Integer)

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