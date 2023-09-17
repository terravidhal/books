from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


# ===== GET ALL BOOKS ======

@app.route("/books")
def create_book(): 
    books = Book.get_all_books()
    return render_template("books.html", all_books=books)


# ===== CREATE BOOKS =========

@app.route("/create_book", methods=['POST'])
def create_book_process(): 

    data = {
        "title": request.form["title"],
        "num_of_pages": request.form["num_of_pages"],
    }

    Book.create_book(data)

    return redirect('/books')



# ===== SHOW SPECIFIC BOOK =========

@app.route("/books/<int:book_id>")
def book_show(book_id):

    data = {
        "book_id" : book_id
    }

    one_book = Book.get_book_with_authors(data)
    #print('+++++++++++++++++++',vars(one_book))

    # ALL AUTHORS
    #authors = Author.get_all_authors()

    # BONUS NINJA : AUTHORS UNFAVORITED BOOKS
    authors = Author.authors_not_favorites_books(data)

    return render_template("show_book.html", one_book = one_book, all_authors=authors)



# ===== ADD FAVORITES AUTHORS WITH SPECIFIC BOOKS =========

@app.route("/process/book", methods=['POST'])
def add_favorites_func_books(): 

    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }

    Author.add_favorites(data)

    return redirect(f'/books/{request.form["book_id"]}')