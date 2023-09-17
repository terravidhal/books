from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book: 
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = [] 


    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"

        results = connectToMySQL('books_database').query_db(query)

        books = []

        for elt in results:
            books.append( cls(elt) )

        return books

    @classmethod
    def create_book(cls, data):
        
        query = "INSERT INTO books ( title, num_of_pages, created_at, updated_at ) VALUES ( %(title)s, %(num_of_pages)s, NOW() , NOW() );"

        return connectToMySQL('books_database').query_db( query, data )
    


    @classmethod
    def get_book_with_authors(cls, data):
        query =""" SELECT * FROM books 
                   LEFT JOIN favorites ON books.id = favorites.book_id 
                   LEFT JOIN authors ON authors.id = favorites.author_id
                   WHERE books.id = %(book_id)s; """

        results = connectToMySQL('books_database').query_db( query, data)

        book = cls(results[0]) 

        for data in results: 
            author_data = {
                "id": data['authors.id'],
                "name": data['name'],
                "created_at": data['authors.created_at'],
                "updated_at": data['authors.updated_at']
            }
            
            new_author_instance = author.Author(author_data)

            book.authors.append(new_author_instance)

        return book
    


    #============ Bonus NINJA 1 ============
    @classmethod
    def books_not_favorites_authors(cls, data):
        query = """
                SELECT * 
                FROM books
                WHERE books.id 
                NOT IN (SELECT book_id FROM favorites WHERE author_id = %(author_id)s)
                ;  """
        books = []
        results = connectToMySQL('books_database').query_db(query, data)
        for elt in results:
            books.append(cls(elt))
        return books