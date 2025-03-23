# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import books

def create_app() -> FastAPI:
    app = FastAPI(title="Library API")

    # Dla przykładu, zezwolenie na wszystkie źródła (wszystkie domeny):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          
        allow_credentials=True,
        allow_methods=["*"],          # ["GET", "POST", "PUT", "DELETE"]
        allow_headers=["*"],          # ["Content-Type", "Authorization", ...]
    )

    # Tworzenie tabeli (jeśli nie istnieją). W produkcji używa się najczęściej migracji Alembic
    Base.metadata.create_all(bind=engine)

    # Rejestracja routerów z trasami dotyczącymi książek
    app.include_router(books.router)

    return app

app = create_app()
