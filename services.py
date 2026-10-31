"""Database operations for creating and managing bookstore books."""

from models import Book
from sqlalchemy.orm import Session
from schemas import BookCreate


def create_book(db: Session, data: BookCreate) -> Book:
    """Create a book record and return the refreshed database object.

    Args:
        db: The database session used for the operation.
        data: Validated fields for the new book.

    Returns:
        The persisted book with database-generated fields populated.
    """
    book_instance = Book(**data.model_dump())
    db.add(book_instance)
    db.commit()
    db.refresh(book_instance)
    return book_instance


def get_books(db: Session):
    """Return all book records.

    Args:
        db: The database session used to query the records.

    Returns:
        A list of all books in the database.
    """
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    """Find a book by its database identifier.

    Args:
        db: The database session used to query the record.
        book_id: Identifier of the book to retrieve.

    Returns:
        The matching book, or ``None`` if no book has that identifier.
    """
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: BookCreate):
    """Replace a book's fields when a matching record exists.

    Args:
        db: The database session used for the operation.
        book_id: Identifier of the book to update.
        book: Validated values to assign to the book.

    Returns:
        The refreshed book if found; otherwise, ``None``.
    """
    book_queryset: Book | None = db.query(Book).filter(Book.id == book_id).first()

    if book_queryset:
        for key, value in book.model_dump().items():
            setattr(book_queryset, key, value)
        db.commit()
        db.refresh(instance=book_queryset)
        return book_queryset


def delete_book(db: Session, book_id: int):
    """Delete a book when a matching record exists.

    Args:
        db: The database session used for the operation.
        book_id: Identifier of the book to delete.

    Returns:
        The deleted book if found; otherwise, ``None``.
    """
    book_queryset: Book | None = db.query(Book).filter(Book.id == book_id).first()
    if book_queryset:
        db.delete(instance=book_queryset)
        db.commit()
        return book_queryset
