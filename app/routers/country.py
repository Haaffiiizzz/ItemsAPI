from fastapi import status, HTTPException, Body, Depends, APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
from contextlib import contextmanager
from ..schemas import AddData
from ..models import Base, Country
from ..oauth2 import getCurrentUser
from ..config import settings


router = APIRouter(tags= ["Countries"])  # tags is for what group it should add it to in the fastapi doc

metadata = MetaData()


Base.metadata.create_all(bind=engine)

@contextmanager
def psycopg2Cursor():
    # this is for use in adding to the countries as I couldnt use sqlalchemy

    conn_params = {
        'dbname': settings.DATABASE_NAME,
        'user': settings.DATABASE_USERNAME,
        'password': settings.DATABASE_PASSWORD,
        'host': settings.DATABASE_HOSTNAME,
        'port': settings.DATABASE_PORT,
        'sslmode': 'require'
    }

    conn = psycopg2.connect(**conn_params, cursor_factory=RealDictCursor)
    try:
        
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    
    except Exception as Ex:
        conn.rollback()
        raise Ex
    
    finally:
        cursor.close()
        conn.close()


@router.get("/")
def root(db: Session = Depends(get_db)):
    # this is the base site without any paths

    countries = db.query(Country).all()
    countryNames = [row.country for row in countries]
    return {"message": f"Welcome to my Items API. Below is a list of all countries available.",
            "countries": countryNames}


@router.get("/countries")
def Get_All_Countries(db: Session = Depends(get_db), limit: int = None):

    countries = db.query(Country).limit(limit).all()
    

    return countries


@router.get("/countries/{country}")
def Get_One_Country(country: str, db: Session = Depends(get_db)):
    #  in this path we should return a json of just a country
    #  and its items and prices
    country = country.title()

    row = db.query(Country).filter(Country.country == country).first()
    #  check if the row is valid i.e country in data base else raise error
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{country} not found")
    #  format the data
    
    return row


@router.put("/countries/{country}", status_code=status.HTTP_201_CREATED)
def Add_Items(country, newData: AddData = Body(...), db: Session = Depends(get_db)):
    #  first check to make sure we have the right data format
    #  send back to user and print data

    # currUser: int = Depends(getCurrentUser), add this to add_items arguements latrer
    country = country.title()

    row = db.query(Country).filter(Country.country == country).first()
    #  check if the row is valid i.e country in data base else raise error
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{country} not found")
    #  format the data
    
    countryItems = row.items
    for item, value in newData.items:
        if item not in countryItems:
            countryItems[item] = value

    row.items = countryItems        
    newItems = Country(**row.items)
    db.add(newItems)
    db.commit()
    db.refresh(newItems)
    return newItems


    # with psycopg2Cursor() as cursor:
    #     cursor.execute(f'SELECT * FROM "Countries" WHERE name = \'{country}\';')
    #     row = cursor.fetchone()

    #     if not row:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f"{country} not found")
    #     # check if the row is valid i.e the country is in the database
        
    #     for itemName in newData.items.keys():
    #         cursor.execute(f"""
    #             DO $$
    #             BEGIN
    #                 IF NOT EXISTS (
    #                     SELECT 1
    #                     FROM information_schema.columns 
    #                     WHERE table_name='Countries' AND column_name= \'{itemName}\'
    #                 ) THEN
    #                     ALTER TABLE "Countries" ADD COLUMN "{itemName}" NUMERIC;
    #                 END IF;
    #             END
    #             $$;
    #         """)
        
    #     #  create new row with the name of the item if the row is not already available
    #     #  note: null will be the value
        
    #     for itemName, itemPrice in newData.items.items():
    #         cursor.execute(
    #             f'UPDATE "Countries" SET "{itemName}" = %s WHERE name = %s;',
    #             (itemPrice, country)
    #         )
        
    # # update the database i.e replace null with the right stuff
    
    return {"Added prices": {"Country" : country.title(), "items": newData}}