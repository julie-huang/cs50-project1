import os
import requests

from flask import Flask, session, render_template, request, redirect, jsonify, flash, url_for
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


def review_counts(isbn):
    url = 'https://www.goodreads.com/book/review_counts.json'
    payload = {'isbns': isbn}
    r = requests.get(url, params=payload)
    r_dict = r.json()['books'][0]
    return r_dict


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


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    flash('You have successfully logged out.')
    return render_template("index.html")


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

# need to fix review functionality
@app.route("/books/<string:isbn>", methods=['GET', 'POST'])
def books(isbn):
    data = db.execute("SELECT * FROM books WHERE isbn=:isbn",
                      {"isbn": isbn}).fetchall()
    r_data = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",
                        {"isbn:isbn"}).fetchall()
    return render_template("books.html", book=data[0], reviews=r_data[0])


@app.route("/api/book/<string:isbn>", methods=['GET'])
def books_api(isbn):

    book = db.execute("SELECT * FROM books where isbn=:isbn",
                      {"isbn": isbn}).fetchone()

    if book is None:
        return jsonify({"error": "Invalid isbn"}), 404

    review_data = review_counts(isbn)

    return jsonify(
        tite=book.title,
        author=book.author,
        year=book.year,
        review_count=review_data['reviews_count'],
        average_score=review_data['average_rating']
    )
