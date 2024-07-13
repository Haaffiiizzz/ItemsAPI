from fastapi import status, HTTPException, Body, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from ..schemas import AddData
from ..models import Base, Country, Country2
from ..oauth2 import getCurrentUser


router = APIRouter(tags= ["Countries"])  
metadata = MetaData()


Base.metadata.create_all(bind=engine)


@router.get("/")
def root(db: Session = Depends(get_db)):
 

    countries = db.query(Country).all()
    countryNames = [row.country for row in countries]
    return {"message": f"Welcome to my Items API. My github username is Haaffiizzz and my LinkedIn is linkedin.com/in/haaffiiizzz. Below is a list of all countries available.",
            "countries": countryNames}


@router.get("/countries")
def Get_All_Countries(db: Session = Depends(get_db), limit: int = None, table: str = "private"):
    if table == "public":
        countries = db.query(Country2).limit(limit).all()
    else:
        countries = db.query(Country).limit(limit).all()

    return countries


@router.get("/countries/{country}")
def Get_One_Country(country: str, db: Session = Depends(get_db), table: str = "private"):
  
    country = country.title()
    if table == "public":
        row = db.query(Country2).filter(Country2.country == country).first()
    else:
        row = db.query(Country).filter(Country.country == country).first()
    #  check if the row is valid i.e country in data base else raise error
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{country} not found")
    #  format the data
    
    return row


@router.put("/countries/{country}", status_code=status.HTTP_201_CREATED)
def Add_Items(country, newData: AddData = Body(...), currUser: int = Depends(getCurrentUser), db: Session = Depends(get_db)):
 
    country = country.title()

    row = db.query(Country2).filter(Country2.country == country).first()
    
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{country} not found")
    
    
    countryItems = row.items
    for item, value in newData.items.items():
        if item not in countryItems:
            countryItems[item] = value

    newRow = Country2(
            country=row.country,
            items=countryItems
        )
        

    db.delete(row)
   
    db.add(newRow)
    db.commit()
    db.refresh(newRow)


    return {"Added prices": {"Country" : country.title(), "items": newRow.items}}
