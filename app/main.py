from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import MetaData
from .models import Base
from .routers import country
from .database import engine


metadata = MetaData()

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(country.router)
# app.include_router(users.router)
# app.include_router(auth.router)    # add the routers from the other files
