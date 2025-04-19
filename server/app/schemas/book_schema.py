from pydantic import BaseModel


class BookCreate(BaseModel):
    """Schema for creating a new book."""

    title: str
    author: str
    year: int
    genre: str


class BookResponse(BaseModel):
    """Schema for book response."""

    id: str
    title: str
    author: str
    year: int
    genre: str
