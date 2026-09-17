from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import foreign

db = SQLAlchemy()

class Author(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

    def __str__(self):
        return f"Author: {self.name}, Date of Birth: {self.birth_date}, has the ID: {self.id}"


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title})"

    def __str__(self):
        return (f"Book: {self.title}, publication_year: {self.publication_year}, has the isbn: {self.isbn}, "
                f"write by the author: {self.author_id}, book_id: {self.id}")


