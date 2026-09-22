from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an ‘authors’ table with the following columns:
    id (primary key), the author’s name as ‘name’, the author’s date of birth as ‘birth_data’
    and the date of death of a deceased author as ‘data_of_death’.

   he class can be printed out itself
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

    def __str__(self):
        return f"Author: {self.name}, Date of Birth: {self.birth_date}, has the ID: {self.id}"


class Book(db.Model):
    """
    Represents a ‘books’ table with the following columns:
    id (primary key), ISBN number, book title, year of publication and author id (foreign key).

    The class can be printed out itself
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, unique=True, nullable=True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title})"

    def __str__(self):
        return (f"Book: {self.title}, publication_year: {self.publication_year}, has the isbn: {self.isbn}, "
                f"write by the author: {self.author_id}, book_id: {self.id}")


