from flask import Flask, render_template, request, redirect, url_for
import os
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/add_author", methods=['GET', 'POST'])
def add_author():

  """
  Provides the user with a website that allows them to add an author to the table.
  Adds a new author to the authors’ table
  """
  message = None

  if request.method == 'POST':
      try:
          name = request.form.get("name")
          birth_date_str = request.form.get("birthdate")
          date_of_death_str = request.form.get("date_of_death")

          birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date() if birth_date_str else None
          date_of_death = datetime.strptime(date_of_death_str, "%Y-%m-%d").date() if date_of_death_str else None

          new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)


          db.session.add(new_author)
          db.session.commit()
          message = f"Autor '{name}' add successfully!"
      except Exception as e:
          db.session.rollback()
          message = f"Error: {e}"

  return render_template('add_author.html', message=message)

@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
  """
  Provides the user with a website that allows them to add a book to the table.
  Adds a new book to the book table
  """
  message = None
  authors = Author.query.order_by(Author.name).all()


  if request.method == 'POST':
    if not authors:
      message = "Please add an author first before adding a book."
      return render_template('add_book.html', message=message, authors=authors)

    title = request.form.get("title")
    publication_year = request.form.get("publication_year")
    isbn = request.form.get("isbn")
    author_id = request.form.get("author_id")

    try:
      publication_year = int(publication_year)
      author_id = int(author_id)

      new_book = Book(title=title, publication_year=publication_year, isbn=isbn, author_id=author_id)
      db.session.add(new_book)
      db.session.commit()
      message = f"Book '{title}' add successfully!"

    except ValueError:
      message = "Invalid year or author selection"

    except Exception as e:
      db.session.rollback()
      message = f"Error: {e}"

    return render_template('add_book.html', message=message, authors=authors)

@app.route("/", methods=['GET'])
def home():
  """
  Displays the home page to the user, showing their book collection from the book table.
  Allow the user to search for a book title and to sort by book title or author name (in descending or ascending order).
  """
  search = request.args.get("search")
  sort_by = request.args.get("sort_by", "title")
  direction = request.args.get("direction", "asc")
  message = request.args.get("message")

  if sort_by == "author":
    query = Book.query.join(Author)
    column = Author.name
  else:
    query = Book.query
    column = Book.title

  if search:
    query = query.filter(Book.title.ilike(f"%{search}%"))

  if direction == "desc":
    column = column.desc()

  books = query.order_by(column).all()

  if search and not books:
    message = "No books found!"
    return render_template('home.html', sort_by=sort_by, direction=direction, message=message)

  return render_template('home.html', books=books, sort_by=sort_by, direction=direction, message=message)

@app.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):

  """
  Deletes a book from the books table when the user clicks the ‘Delete’ button on the website.

  Records the author ID of the deleted book.
  It then scans the books table; if an author’s ID no longer appears there,
  the function also deletes the author from the authors table.
  """
  book = db.session.get(Book, book_id)

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
    app.run(host="0.0.0.0", port=5003, debug=True)