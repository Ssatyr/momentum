# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import logging

from ..models import Book
from ..schemas import BookCreate, BookOut, BorrowRequest
from ..dependencies import get_db

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()

@router.post("/books", response_model=BookOut, summary="Dodaj nową książkę")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create book with serial number: {book_data.serial_number}")
    
    existing_book = db.query(Book).filter(Book.serial_number == book_data.serial_number).first()
    if existing_book:
        logger.warning(f"Book with serial number {book_data.serial_number} already exists")
        raise HTTPException(status_code=400, detail="Książka o podanym numerze seryjnym już istnieje.")

    new_book = Book(
        serial_number=book_data.serial_number,
        title=book_data.title,
        author=book_data.author
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    logger.info(f"Successfully created book: {book_data.title} ({book_data.serial_number})")
    return new_book

@router.delete("/books/{serial_number}", summary="Usuń książkę")
def delete_book(serial_number: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to delete book with serial number: {serial_number}")
    
    book = db.query(Book).filter(Book.serial_number == serial_number).first()
    if not book:
        logger.warning(f"Book with serial number {serial_number} not found")
        raise HTTPException(status_code=404, detail="Książka o podanym numerze seryjnym nie istnieje.")

    db.delete(book)
    db.commit()
    logger.info(f"Successfully deleted book with serial number: {serial_number}")
    return {"message": f"Książka o numerze seryjnym {serial_number} została usunięta."}

@router.get("/books", response_model=List[BookOut], summary="Pobierz listę wszystkich książek")
def get_all_books(db: Session = Depends(get_db)):
    logger.info("Fetching all books")
    books = db.query(Book).all()
    logger.info(f"Retrieved {len(books)} books")
    return books

@router.put("/books/{serial_number}/borrow", response_model=BookOut, summary="Wypożycz książkę")
def borrow_book(serial_number: str, request: BorrowRequest, db: Session = Depends(get_db)):
    logger.info(f"Attempting to borrow book {serial_number} by user {request.library_card_number}")
    
    book = db.query(Book).filter(Book.serial_number == serial_number).first()
    if not book:
        logger.warning(f"Book with serial number {serial_number} not found")
        raise HTTPException(status_code=404, detail="Książka o podanym numerze seryjnym nie istnieje.")

    if book.is_borrowed:
        logger.warning(f"Book {serial_number} is already borrowed")
        raise HTTPException(status_code=400, detail="Książka jest już wypożyczona.")

    book.is_borrowed = True
    book.borrowed_by = request.library_card_number
    book.borrowed_at = datetime.utcnow()
    db.commit()
    db.refresh(book)
    logger.info(f"Successfully borrowed book {serial_number} to user {request.library_card_number}")
    return book

@router.put("/books/{serial_number}/return", response_model=BookOut, summary="Zwróć książkę")
def return_book(serial_number: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to return book {serial_number}")
    
    book = db.query(Book).filter(Book.serial_number == serial_number).first()
    if not book:
        logger.warning(f"Book with serial number {serial_number} not found")
        raise HTTPException(status_code=404, detail="Książka o podanym numerze seryjnym nie istnieje.")

    if not book.is_borrowed:
        logger.warning(f"Book {serial_number} is not borrowed")
        raise HTTPException(status_code=400, detail="Książka jest już dostępna (nie jest wypożyczona).")

    book.is_borrowed = False
    book.borrowed_by = None
    book.borrowed_at = None
    db.commit()
    db.refresh(book)
    logger.info(f"Successfully returned book {serial_number}")
    return book
