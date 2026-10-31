"""FastAPI application for the bookstore API.

Imports:
- asynccontextmanager from contextlib to initialize the database during app startup.
- FastAPI, Depends, and HTTPException from fastapi for creating the API app,
  dependency injection, and HTTP error responses.
- services, models, and schemas for business logic, database models, and request/response validation.
- get_db and create_table from db for database sessions and table initialization.
- Session from sqlalchemy.orm for type annotations on database sessions.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
import services, models, schemas
from db import get_db, create_table
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create missing database tables before serving API requests."""
    create_table()
    yield


# Create the FastAPI application instance that exposes the API routes.
app = FastAPI(lifespan=lifespan)


# Fetch all books from the database and return them as a list of Book schema objects.
@app.get("/books", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(dependency=get_db)):
    return services.get_books(db)


# Retrieve a single book by its ID. If no match is found, return a 404 error.
@app.get("/books/{id}", response_model=schemas.Book)
async def get_book_by_id(id: int, db: Session = Depends(dependency=get_db)):
    book_queryset = services.get_book(db, id)
    if book_queryset:
        return book_queryset
    raise HTTPException(
        status_code=404, detail="Invalid Book ID Provided or Book id does not exist"
    )


# Create a new book record using the data passed in the request body.
@app.post("/books", response_model=schemas.Book)
async def create_new_book(
    book: schemas.BookCreate, db: Session = Depends(dependency=get_db)
):
    return services.create_book(db, book)


# Update an existing book by ID. If the book does not exist, return a 404.
@app.put("/books/{id}", response_model=schemas.Book)
async def update_book(
    book: schemas.BookCreate, id: int, db: Session = Depends(dependency=get_db)
):
    db_update = services.update_book(db, book, id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_update


# Delete a book by ID and return the deleted record if successful.
@app.delete("/books/{id}", response_model=schemas.Book)
async def delete_book(id: int, db: Session = Depends(dependency=get_db)):
    delete_entry = services.delete_book(db, id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail="Book not found")
