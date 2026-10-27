from db import Base
from pydantic import BaseModel


class BookBase(BaseModel):
    """Base class for Book models.

    Inputs: None.
    Output: A Pydantic model base class.
    Why: Provide a shared base class for all Book models.
    """

    title: str
    description: str
    author: str
    year: int


class BookCreate(BookBase):
    """Model for creating a new Book record.

    Inputs: None.
    Output: A Pydantic model for creating a Book.
    Why: Validate input data when creating a new Book record.
    """

    pass


class Book(BookBase):
    """Model for reading a Book record.

    Inputs: None.
    Output: A Pydantic model for reading a Book.
    Why: Validate output data when returning a Book record.
    """

    id: int

    class Config:
        orm_mode = True
        from_attributes = True
