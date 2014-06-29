from flask import Flask
import subprocess
import random

app = Flask(__name__)

@app.route("/")
def hello():
	data = random.random()
	return str(data)

