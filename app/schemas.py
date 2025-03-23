# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Annotated

class BookCreate(BaseModel):
    serial_number: Annotated[str, Field(min_length=6, max_length=6, pattern=r'^\d{6}$')]
    title: str
    author: str

class BookBase(BaseModel):
    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_at: Optional[datetime]
    borrowed_by: Optional[str]

class BookOut(BookBase):
    pass

class BorrowRequest(BaseModel):
    library_card_number: Annotated[str, Field(min_length=6, max_length=6, pattern=r'^\d{6}$')]
