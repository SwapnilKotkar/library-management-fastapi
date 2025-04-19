from app.core.database import db
from app.models.book_model import BookModel

books_collection = db["books"]


async def add_book(data: dict):
    new_book = await books_collection.insert_one(data)
    return new_book


async def get_books():
    books = await books_collection.find().to_list(100)
    return books
