from flask import Flask, render_template, request, jsonify, make_response
from subprocess import Popen, PIPE, STDOUT
import os
import random
import hashlib
import psycopg2

app = Flask(__name__, static_url_path = "")

@app.route("/")
def hello():
	data = random.random()
	return render_template('home.html')

@app.route("/code")
def code():
	print "here"
	print random.random()
	unique_hash = str(hashlib.sha224(str(random.random())).hexdigest())
	return render_template('main.html',url=unique_hash)

@app.route("/save",methods=['POST'])
def save_code():
	code = str(request.form['CODE'])
	email = str(request.form['EMAIL'])
	comments = str(request.form['COMMENTS'])
	unique_hash = str(request.form['HASH'])

	STATUS = "TRUE"
	try:
		conn = psycopg2.connect(
		database="dhgab48kaqk79",
		user="wgciyahtsvsaxi",
		password="8NIfTLHTetrg_xYjwmA_LKr36w",
		host="ec2-54-225-135-30.compute-1.amazonaws.com",
		port="5432")

		#get a cursor
		print "Writing to DB"
		cursor = conn.cursor()
		query =  """INSERT INTO data (hash,email,code,comments) VALUES(\'%s\',\'%s\',\'%s\',\'%s\');"""%(unique_hash,email,code,comments)
		print query
		cursor.execute(query)

	except:
		print "Connection Failed,Informing client"
		STATUS = FALSE

	return jsonify({'STATUS' , STATUS})



if __name__ == "__main__":
	app.run()

