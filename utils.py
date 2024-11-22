from typing import Optional
from sqlalchemy import create_engine
from sqlmodel import Session, select
from bookstore.models import Author, Book



engine = create_engine("sqlite:///database.db")

def get_books_for_author(first_name: str, last_name: str):
    with Session(engine) as session:
        statement = select(Author).where(Author.first_name == first_name, Author.last_name == last_name)
        author = session.exec(statement).first()

        statement = select(Book).where(Book.author_id == author.id)

        books = session.exec(statement=statement).all()

        return [book.name for book in books]


def get_book_id_by_title(title: str) -> Optional[int]:
    with Session(engine) as session:
        statement = select(Book).where(Book.name == title)
        book = session.exec(statement).first()
        if book and book.id:
            return book.id
        return None


def get_num_in_stock_for_book(title: str) -> int:
    with Session(engine) as session:
        statement = select(Book).where(Book.name == title)
        book = session.exec(statement).first()
        if book:
            return book.num_in_stock
        return 0
