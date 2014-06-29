from flask import Flask,render_template
import subprocess
import random

app = Flask(__name__)

@app.route("/")
def hello():
	data = random.random()
	return render_template("main.html")

