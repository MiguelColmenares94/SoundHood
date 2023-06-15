#!usr/bin/python3
""" Module for all the routes managed by the app """

from soundhood import app


@app.route("/")
@app.route("/home/")
def home_page():
    """ Show the home page URL """
    return "<h1> Home page </h1>"


@app.route("/login/")
def enter():
    """ Show the log in URL """
    return "<h1> Log in  </h1>"


@app.route("/register/")
def register():
    """ Show the register URL """
    return "<h1> Register  </h1>"


@app.route("/user_profile/")
def log_in():
    """ Show the user profile URL """
    return "<h1> User Profile </h1>"
