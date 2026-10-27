"""Define the database model for books in the bookstore."""

# Import the shared SQLAlchemy base so this model is registered with the app's metadata.
from db import Base
# Import column types and the column constructor used to describe book fields.
from sqlalchemy import Integer,Column,String

class Book(Base):
    """Represent a book record stored in the `books` database table."""

    # Map this model to the table used to persist bookstore books.
    __tablename__ = "Books"

    # Store each book's identifier and searchable descriptive information.
    id= Column(Integer, primary_key=True, Index=True)
    title= Column(String,index=True)
    description= Column(String,index=True)
    author= Column(String,index=True)

    # Record the book's publication year as an integer.
    year= Column(Integer)

