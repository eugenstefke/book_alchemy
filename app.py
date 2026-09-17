from email import message

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

with app.app_context():
  db.create_all()

@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
  message = None

  if request.method == 'POST':
    name = request.form.get("name")
    birth_date = request.form.get("birthdate")
    date_of_death = request.form.get("date_of_death")

    new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

    db.session.add(new_author)
    db.session.commit()

    message = f"Autor '{name}' add successfully!"

  return render_template('add_author.html', message=message)

@app.route("/add_book", methods=['GET', 'POST'])
def add_book():

  message = None

  if request.method == 'POST':
    title = request.form.get("title")
    publication_year = request.form.get("publication_year")
    isbn = request.form.get("isbn")
    author_id = request.form.get("author_id")

    new_book = Book(title=title, publication_year=publication_year, isbn=isbn, author_id=author_id)

    db.session.add(new_book)
    db.session.commit()


    message = f"Book'{title}' add successfully!"
  authors = Author.query.all()
  return render_template('add_book.html', message=message, authors=authors)

@app.route("/", methods=['GET'])
def home():

  search = request.args.get("title")
  sort_by = request.args.get("sort_by", "title")
  direction = request.args.get("direction", "asc")
  message = request.args.get("message")

  if sort_by == "author":
    query = Book.query.join(Author)
    column = Author.name
  else:
    query = Book.query
    column = Book.title

  if direction == "desc":
    column = column.desc()

  books = query.order_by(column).all()
  authors = Author.query.all()

  if search:
    books = Book.query.filter(Book.title.like(f"%{search}%")).all()
    if not books:
      message = f"No books found!"
      return render_template('home.html', message=message)

  return render_template('home.html', books=books, sort_by=sort_by, direction=direction, authors=authors, message=message)

@app.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
  book = Book.query.filter_by(id=book_id).first()

  if book is None:
    return redirect(url_for('home', message="Book not found!"))

  title = book.title # save title for message
  author_id = book.author_id  # note author_id befor delete book

  db.session.delete(book)
  db.session.commit()

  # Check if no more books have the same author_id
  remaining_books = Book.query.filter_by(author_id=author_id).all()

  if not remaining_books:
    db.session.delete(Author.query.get(author_id))
    db.session.commit()

  message = f"Book '{title}' was deleted successfully!"
  return redirect(url_for('home', message=message))

if __name__ == "__main__":
    # host="0.0.0.0" macht die App auch außerhalb von localhost erreichbar (z. B. in Codio)
    app.run(host="0.0.0.0", port=5000, debug=True)