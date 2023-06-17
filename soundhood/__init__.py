#!/usr/bin/python3
from flask import Flask


app = Flask(__name__)
app.app_context().push()

from soundhood import routes
