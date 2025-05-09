from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name}, birth_date = {self.birth_date}, date_of_death = {self.date_of_death})"

    def __str__(self):
        return f"Author: {self.name}"


class Book(db.Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(Integer)
    title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('author.id'))

    def __repr__(self):
        return f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title}, publication_year = {self.publication_year}, author_id = {self.author_id})"

    def __str__(self):
        return f"Book title: {self.title}"

