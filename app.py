from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'library.sqlite')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    """This function handles form submission for adding a new author to the database."""
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            birthdate = None
        try:
            date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None
        except (ValueError, TypeError):
            date_of_death = None
        new_author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)
        try:
            db.session.add(new_author)
            db.session.commit()
            print(f"Author '{name}' added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add author: {str(e)}")
    return render_template('add_author.html')


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    """This function handles form submission for adding a new book with an associated author."""

    # List of authors for the dropdown
    authors = Author.query.all()

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id
        )
        try:
            db.session.add(new_book)
            db.session.commit()
            print(f"Book '{title}' added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding book: {str(e)}")
    return render_template('add_book.html', authors=authors)


@app.route("/")
def home():
    """This function displays all books with their authors on the homepage, with optional sorting."""
    sort_by = request.args.get("sort", "title")
    search_term = request.args.get("search", "").strip()

    query = db.session.query(Book.title, Book.isbn, Author.name.label('author_name')) \
        .join(Author, Book.author_id == Author.id)

    if search_term:
        query = query.filter(Book.title.ilike(f"%{search_term}%"))
    if sort_by == "author":
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()
    no_results = not books and search_term

    return render_template("home.html", books=books, no_results=no_results, search_term=search_term)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
