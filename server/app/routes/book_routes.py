from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.book_schema import BookCreate, BookResponse
from app.services import book_service
from app.core import auth, dependencies
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/books", response_model=BookResponse)
@limiter.limit("5/minute")
async def create_book(
    book: BookCreate,
    request: Request,
    current_user: str = Depends(dependencies.require_role("ADMIN")),
):
    new_book = await book_service.add_book(book.model_dump())
    return BookResponse(**new_book.__dict__)


@router.get("/books", response_model=list[BookResponse])
@limiter.limit("10/minute")
async def list_books(
    request: Request, current_user: str = Depends(dependencies.require_role("USER"))
):
    books = await book_service.get_books()
    return [BookResponse(**book.dict()) for book in books]
