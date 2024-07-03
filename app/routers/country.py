from fastapi import status, HTTPException, Body, Depends, APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
from contextlib import contextmanager
from ..schemas import AddData
from ..models import Base
from ..oauth2 import getCurrentUser
from ..config import settings


router = APIRouter(tags= ["Countries"])  # tags is for what group it should add it to in the fastapi doc

# metadata = MetaData()
# countriesTable = Table('Countries1', metadata, autoload_with=engine)


# Base.metadata.create_all(bind=engine)

# @contextmanager
# def psycopg2Cursor():
#     # this is for use in adding to the countries as I couldnt use sqlalchemy

#     conn_params = {
#         'dbname': settings.DATABASE_NAME,
#         'user': settings.DATABASE_USERNAME,
#         'password': settings.DATABASE_PASSWORD,
#         'host': settings.DATABASE_HOSTNAME,
#         'port': settings.DATABASE_PORT,
#         'sslmode': 'require'
#     }

#     conn = psycopg2.connect(**conn_params, cursor_factory=RealDictCursor)
#     try:
        
#         cursor = conn.cursor()
#         yield cursor
#         conn.commit()
    
#     except Exception as Ex:
#         conn.rollback()
#         raise Ex
    
#     finally:
#         cursor.close()
#         conn.close()


# @router.get("/")
# def root(db: Session = Depends(get_db)):
#     # this is the base site without any paths

#     countries = db.query(countriesTable).all()
#     countryNames = [row.name for row in countries]
#     return {"message": f"Welcome to my Items API. Below is a list of all countries available.",
#             "countries": countryNames}


# @router.get("/countries")
# def Get_All_Countries(db: Session = Depends(get_db), limit: int = None):

#     countries = db.query(countriesTable).limit(limit).all()
#     result = [{column.name: getattr(row, column.name) for column in countriesTable.columns} for row in countries]
#     # result is a list of dicts, with each cloumn name in the table as key
#     # and the items in the columns as values
#     resultDict = {}
#     for Dict in result:
#         name = Dict["name"]
#         itemsDict = {key:value for key, value in Dict.items() if key != "name"}
#         resultDict[name] = itemsDict

#     return resultDict


# @router.get("/countries/{country}")
# def Get_One_Country(country: str, db: Session = Depends(get_db)):
#     #  in this path we should return a json of just a country
#     #  and its items and prices
#     country = country.title()

#     row = db.query(countriesTable).filter(countriesTable.c.name == country).first()
#     #  check if the row is valid i.e country in data base else raise error
#     if not row:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{country} not found")
#     #  format the data
#     rowDict = {column: value for column, value in zip(countriesTable.columns.keys(), row)}
#     items = {key: value for key, value in rowDict.items() if key != 'name'}
#     return {"Country": country, "Items": items}


# @router.put("/countries/{country}", status_code=status.HTTP_201_CREATED)
# def Add_Items(country, newData: AddData = Body(...), currUser: int = Depends(getCurrentUser)):
#     #  first check to make sure we have the right data format
#     #  send back to user and print data

    
#     country = country.title()
#     with psycopg2Cursor() as cursor:
#         cursor.execute(f'SELECT * FROM "Countries1" WHERE name = \'{country}\';')
#         row = cursor.fetchone()

#         if not row:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"{country} not found")
#         # check if the row is valid i.e the country is in the database
        
#         for itemName in newData.items.keys():
#             cursor.execute(f"""
#                 DO $$
#                 BEGIN
#                     IF NOT EXISTS (
#                         SELECT 1
#                         FROM information_schema.columns 
#                         WHERE table_name='Countries1' AND column_name= \'{itemName}\'
#                     ) THEN
#                         ALTER TABLE "Countries1" ADD COLUMN "{itemName}" NUMERIC;
#                     END IF;
#                 END
#                 $$;
#             """)
        
#         #  create new row with the name of the item if the row is not already available
#         #  note: null will be the value
        
#         for itemName, itemPrice in newData.items.items():
#             cursor.execute(
#                 f'UPDATE "Countries1" SET "{itemName}" = %s WHERE name = %s;',
#                 (itemPrice, country)
#             )
        
#     # update the database i.e replace null with the right stuff
    
#     return {"Added prices": {"Country" : country.title(), "items": newData}}