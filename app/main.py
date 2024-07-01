from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Table, MetaData
from .models import Base
from .routers import users, country, auth
from .database import engine


metadata = MetaData()
countriesTable = Table('Countries1', metadata, autoload_with=engine)

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(country.router)
app.include_router(users.router)
app.include_router(auth.router)    # add the routes from the other files