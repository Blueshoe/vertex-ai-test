from random import randrange

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from bookstore.factories import AuthorFactory, BookFactory


def create_authors():
    for i in range(0, 1000):
        author = AuthorFactory.build()
        with Session(engine) as session:
            session.add(author)
            session.commit()
            for i in range(1, randrange(1, 10)):
                create_book(author_id=author.id)


def create_book(author_id):
    book = BookFactory.build(author_id=author_id)
    with Session(engine) as session:
        session.add(book)
        session.commit()


engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

create_authors()
# create_books()
