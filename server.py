from flask_app.controllers import authors, books
#remember to import all controllers
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)