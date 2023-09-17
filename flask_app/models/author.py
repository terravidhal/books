from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book


class Author: 
    db = "books_database"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = [] 

    
    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"

        results = connectToMySQL('books_database').query_db(query)

        authors = []

        for elt in results:
            authors.append( cls(elt) )

        return authors


    @classmethod
    def create_author(cls, data):
        
        query = "INSERT INTO authors ( name , created_at, updated_at ) VALUES ( %(name)s, NOW() , NOW() );"

        return connectToMySQL('books_database').query_db( query, data )
    



    @classmethod
    def get_author_with_books(cls, data):
        query = """ SELECT * FROM authors 
                    LEFT JOIN favorites ON authors.id = favorites.author_id 
                    LEFT JOIN books ON books.id = favorites.book_id
                    WHERE authors.id = %(author_id)s; """

        results = connectToMySQL('books_database').query_db( query, data)

        author = cls(results[0]) 

        for data in results: 

            book_data = {
                "id" : data['books.id'],
                "title": data["title"],
                "num_of_pages": data['num_of_pages'],
                "created_at": data["books.created_at"],
                "updated_at": data["books.updated_at"]
            }
            
            new_instance_book = book.Book(book_data)

            author.books.append(new_instance_book)

        return author
    


    @classmethod
    def add_favorites(cls, data):
        
        query = "INSERT INTO favorites ( author_id, book_id ) VALUES ( %(author_id)s, %(book_id)s);"

        return connectToMySQL('books_database').query_db( query, data )
    


    #============ Bonus NINJA 2 ============
    @classmethod
    def authors_not_favorites_books(cls, data):
        query = """
                SELECT * 
                FROM authors
                WHERE authors.id 
                NOT IN (SELECT author_id FROM favorites WHERE book_id = %(book_id)s)
                ; """
        books = []
        results = connectToMySQL('books_database').query_db(query, data)
        for elt in results:
            books.append(cls(elt))
        return books






   

  