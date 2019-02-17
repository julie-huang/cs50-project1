import os
import requests

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

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

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login():
    error=""
    # get form info
    if request.method =='POST':
        username=request.form['username']
        password=request.form['password']
        user=db.execute("SELECT * FROM users WHERE username=:username and password=:password",{"username":username,"password":password}).fetchone()

        if user is None:
            error="Invalid login, please try again"
            return render_template("error.html", message=error)
        else:
            session['logged_in']=True
            return render_template("home.html")

    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")