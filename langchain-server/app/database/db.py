from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://recipe-recommend-db-manager:12345@localhost:3306/recipe-recommend-db?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

Base = SQLModel