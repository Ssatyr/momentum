# app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Odczytujemy zmienną środowiskową z docker-compose (lub lokalnie)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://library_user:library_password@localhost:5432/library_db"
)

# Tworzymy silnik bazy danych
engine = create_engine(DATABASE_URL, echo=True)

# Tworzymy klasę Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla naszych modeli
Base = declarative_base()
