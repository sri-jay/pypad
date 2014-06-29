from flask import Flask
from flask import render_template
import subprocess
import random

app = Flask(__name__, static_url_path = "static")

@app.route("/")
def hello():
	data = random.random()
	return render_template('main.html')

