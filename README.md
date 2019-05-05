## Project 1 from CS50's Web Programming with Python and JavaScript Course 

<https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/>

#### Book Review Website 

#### To set up the database: 

1. Navigate to https://www.heroku.com/, and create an account if you don’t already have one. Click "new and choose "Create new app."

2. On your app’s “Overview” page, click the “Configure Add-ons” button.
In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision." then click the“Heroku Postgres :: Database” link.

3. You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. You can access the database via Adminer, filling in the server (the “Host” in the credentials list), your username (the “User”), your password, and the name of the database, all of which you can find on the Heroku credentials page.

* Alternatively, if you install PostgreSQL on your own computer, you should be able to run psql URI on the command line, where the URI is the link provided in the Heroku credentials list.


#### To set up Python and Flask: 

1. First, make sure you install a copy of Python. For this course, you should be using Python version 3.6 or higher.
2. You’ll also need to install pip. If you downloaded Python from Python’s website, you likely already have pip installed (you can check by running pip in a terminal window). If you don’t have it installed, be sure to install it before moving on!

#### To run the Flask application: 

1. Download the project1 distribution directory from https://cdn.cs50.net/web/2018/spring/projects/1/project1.zip and unzip it.

2. Navigate to `project1` directory in a Terminal window and run `pip3 install -r requirements.txt` to make sure that all of the necessary Python packages (Flask and SQLAlchemy, for instance) are installed.

3. Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this enter in `export FLASK_APP=application.py`. On Windows, the command is instead `set FLASK_APP=application.py`. You may optionally want to set the environment variable `export FLASK_DEBUG=1`, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.

4. Set the environment variable `DATABASE_URL` to be the URI of your database, which you should be able to see from the credentials page on Heroku.

5. Run `flask run` to start up your Flask application.

#### To link with Goodreads API: 

1. Go to https://www.goodreads.com/api and sign up for a Goodreads account if you don’t already have one.

2. Navigate to https://www.goodreads.com/api/keys and apply for an API key. For “Application name” and “Company name” feel free to just write “project1,” and no need to include an application URL, callback URL, or support URL.You should be able to see your API from there. 

3. You can now use that API key to make requests to the Goodreads API, documented [here](https://www.goodreads.com/api/index). In particular, Python code like the below: 

```
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
print(res.json())
```
