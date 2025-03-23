# app/models.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from .db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(6), unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_borrowed = Column(Boolean, default=False)
    borrowed_at = Column(DateTime, nullable=True)
    borrowed_by = Column(String(6), nullable=True)
