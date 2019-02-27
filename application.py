import os
import requests

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config["DEBUG"] = True

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = db.execute("SELECT username, password FROM users WHERE username=:username and password=:password",
                          {"username": username, "password": password}).fetchall()
        if user != []:
            error = "Username has already been taken. Please choose another one."
            return render_template("error.html", message=error)
        else:
            db.execute(('INSERT INTO users (username, password, email)'
                        'VALUES (:username, :password, :email)'),
                       {"username": username, "password": password, "email": email})
            db.commit()
            session["username"] = True
            return render_template("search.html")
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    # get form info
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.execute("SELECT * FROM users WHERE username=:username and password=:password",
                          {"username": username, "password": password}).fetchone()

        if user is None:
            error = "Invalid username and or password, please try again"
            return render_template("error.html", message=error)
        else:
            session['username'] = True
            return render_template("search.html")

    return render_template("login.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
    error = ""
    name = request.form.get('username')
    # if we are putting a search
    if request.method == 'POST':
        q = request.form['q']
        search_query = '%' + q + '%'
        data = db.execute(
            "SELECT * FROM books WHERE title ILIKE (:q) OR isbn ILIKE (:q) or author ILIKE (:q)", {'q': search_query}).fetchall()

        #  see if the data is retrieved
        for d in data:
            print(f"{d.title}")

        if data is None:
            error = "No matches found!"
            return render_template("error.html", message=error)
        else:
            return render_template("result.html", results=data)

    return render_template("search.html", results=data, name=name)


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/books/<string:isbn>", methods=['GET', 'POST'])
def books(isbn):
    data = db.execute("SELECT * FROM books WHERE isbn=:isbn",
                      {"isbn": isbn}).fetchall()
    return render_template("books.html", book=data[0])


@app.route("/api/book/<string:isbn>", methods=['GET'])
def books_api(isbn):

      # Make sure flight exists.
    book = db.execute("SELECT * FROM books where isbn=:isbn",
                      {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 404

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
        # "review_count": db.execute("SELECT review_count from books where isbn=:isbn {"isbn": isbn}).fetchall()
        # "average_score": db.execute("SELECT title from books where isbn=:isbn {"isbn": isbn}).fetchall()
    })
