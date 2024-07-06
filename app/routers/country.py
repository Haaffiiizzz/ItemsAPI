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
    print("first row", row)

    countryItems = row.items
    print(countryItems)
    for item, value in newData.items.items():
        if item not in countryItems:
            countryItems[item] = value
    print("second countryitems", countryItems)

    row.items = countryItems
    print("row.items", row.items)
    print("row:", row)        
    
    newRow = Country(row)
    db.add(newRow)
    db.commit()
    db.refresh(newRow)


    return {"Added prices": {"Country" : country.title(), "items": row.items}}