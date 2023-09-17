from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

# ========== HOME ============

@app.route("/")
def home():
    return redirect("/authors")


# ===== GET ALL AUTHORS ======

@app.route("/authors")
def authors_func():
    authors = Author.get_all_authors()
    return render_template("authors.html", all_authors=authors)


# ===== CREATE AUTHOR =========

@app.route("/create_author", methods=['POST'])
def create_author_process(): 

    data = {
        "name": request.form["Name"],
    }

    Author.create_author(data)

    return redirect('/authors')


# ===== SHOW SPECIFIC AUTHOR =========

@app.route("/authors/<int:author_id>")
def show_specific_author(author_id):

    data = {
        "author_id" : author_id
    }

    one_author = Author.get_author_with_books(data)
    #print('+++++++++++++++++++',vars(one_author))
    
    # ALL BOOKS
    #books = Book.get_all_books()

    # BONUS NINJA : BOOKS UNFAVORITED AUTHORS
    books = Book.books_not_favorites_authors(data)
    

    return render_template("show_author.html", one_author = one_author, all_books=books)




# ===== ADD FAVORITES BOOK WITH SPECIFIC AUTHOR =========

@app.route("/process/author", methods=['POST'])
def add_favorites_func_authors(): 

    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }

    Author.add_favorites(data)

    return redirect(f'/authors/{request.form["author_id"]}')