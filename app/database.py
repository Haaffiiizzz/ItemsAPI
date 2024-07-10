from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# here we just kinda start the database 
DATABASE_URL = os.getenv("DATABASE_URL")

# Use the environment variable directly
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# SQL_DB_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?sslmode=require"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(SQL_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()


