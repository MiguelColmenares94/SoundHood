#!/usr/bin/python3
from flask import Flask, session
from secrets import token_hex


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = token_hex()

from soundhood import routes
