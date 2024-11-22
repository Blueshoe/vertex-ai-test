from faker import Faker
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from bookstore.models import Author, Book


class AuthorFactory(ModelFactory[Author]):
    __model__ = Author
    __faker__ = Faker(locale="de_DE")
    id = Use(lambda: None)

    @classmethod
    def first_name(cls) -> str:
        return cls.__faker__.first_name()

    @classmethod
    def last_name(cls) -> str:
        return cls.__faker__.last_name()
    


class BookFactory(ModelFactory[Book]):
    __model__ = Book
    __faker__ = Faker(locale="de_DE")
    id = Use(lambda: None)

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.catch_phrase()

