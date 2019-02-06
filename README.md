# Project 1 from CS50's Web Programming with Python and JavaScript Course 

<https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/>

Web Programming with Python and JavaScript

To setup the project: 

For this project, you’ll need to set up a PostgreSQL database to use with our application. It’s possible to set up PostgreSQL locally on your own computer, but for this project, we’ll use a database hosted by Heroku, an online web hosting service.

Navigate to https://www.heroku.com/, and create an account if you don’t already have one.
On Heroku’s Dashboard, click “New” and choose “Create new app.”
Give your app a name, and click “Create app.”
On your app’s “Overview” page, click the “Configure Add-ons” button.
In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
Now, click the “Heroku Postgres :: Database” link.
You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. You can access the database via Adminer, filling in the server (the “Host” in the credentials list), your username (the “User”), your password, and the name of the database, all of which you can find on the Heroku credentials page.
Alternatively, if you install PostgreSQL on your own computer, you should be able to run psql URI on the command line, where the URI is the link provided in the Heroku credentials list.


1. cd into the project directory
2. Run `pip3 install -r requirements.txt` to make sure all the necessary packages are installed on your machine
3. On a Mac or on Linux, to set the environment variable for `FLASK_APP` type `export FLASK_APP=application.py` into the command line. On Windows, the command is instead set `FLASK_APP=application.py`. You may optionally want to set the environment variable `export FLASK_DEBUG=1`, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.
4. Enter in `export DATABASE_URL =` to URI of your database, which you should be able to see from the credentials page on Heroku. 
5. Run `flask run` to start up your Flask application.


