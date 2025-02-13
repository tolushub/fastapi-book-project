from typing import OrderedDict
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from ..db.schemas import Book, Genre, InMemoryDB

# Initialize the router
router = APIRouter()

# Initialize the in-memory database
db = InMemoryDB()

# Pre-populate the in-memory database with some books
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Shits",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

# Endpoint to create a new book
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

# Endpoint to get all books
@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK
)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()

# Endpoint to update a book by ID
@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    updated_book = db.update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_book.model_dump(),
    )

# Endpoint to delete a book by ID
@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int):
    """
    Delete a book by its ID.
    """
    if not db.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return None  # Return nothing for 204 No Content

# Endpoint to retrieve a book by ID
@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Retrieve a book by its ID.
    """
    book = db.get_books().get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book