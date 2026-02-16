import sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_FOLDER = os.path.join(os.path.dirname(__file__), "db"),
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FOLDER}/database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()