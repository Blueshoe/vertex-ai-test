from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    birthday: date


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    author_id: int = Field(default=None, foreign_key="author.id")
    num_in_stock: int = 0
