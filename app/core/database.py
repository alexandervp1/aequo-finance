#Engine for SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

#Our clases (models) for tables in database.
import app.models.financial 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create all tables if not exists.
def init_db():
    Base.metadata.create_all(bind=engine)



