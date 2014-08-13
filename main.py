from flask import Flask, render_template, request, jsonify, make_response
from subprocess import Popen, PIPE, STDOUT
import os
import random
import hashlib
import psycopg2
import json
import urlparse

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

@app.route("/home")
def home():
	return render_template('recent.html')

@app.route("/get_all_codes",methods=['GET','POST'])
def get_all_codes():
	try:
		conn = psycopg2.connect(
		database="dhgab48kaqk79",
		user="wgciyahtsvsaxi",
		password="8NIfTLHTetrg_xYjwmA_LKr36w",
		host="ec2-54-225-135-30.compute-1.amazonaws.com",
		port="5432")

		cursor = conn.cursor()
		query = """SELECT hash FROM data"""
		print query
		cursor.execute(query)
		code = cursor.fetchall()
		print code
	except Exception as e:
		print e

	return jsonify( {'hashes' : code} )

@app.route("/save",methods=['POST'])
def save_code():
	_code_ = request.form['CODE']
	_email_ = request.form['EMAIL']
	_comments_ = request.form['COMMENTS']
	_unique_hash_ = request.form['HASH']

	_code_ = _code_.replace("'","\"")

	print _code_
	print _email_
	print _comments_
	print _unique_hash_

	STATUS = "TRUE"
	
	print "\n"
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
		query =  """INSERT INTO data VALUES(\'%s\',\'%s\',\'%s\',\'%s\');"""%(_unique_hash_,_email_,_code_,_comments_)
		print query
		cursor.execute(query)
		conn.commit()

	except Exception as e:
		print "Connection Failed,Informing client"
		print e
		STATUS = "FALSE"

	return jsonify({'STATUS' : STATUS})

@app.route("/get/<data>",methods=['GET','POST'])
def get_code(data):
	code_hash = data
	print data
	try:
		conn = psycopg2.connect(
		database="dhgab48kaqk79",
		user="wgciyahtsvsaxi",
		password="8NIfTLHTetrg_xYjwmA_LKr36w",
		host="ec2-54-225-135-30.compute-1.amazonaws.com",
		port="5432")

		cursor = conn.cursor()
		query = """SELECT * FROM data where hash=\'%s\'"""%(code_hash)
		print query
		cursor.execute(query)
		code = cursor.fetchone()
		print code
	except Exception as e:
		print e

	return jsonify( {'CODE' : code[2],'EMAIL' : code[1],'COMMENTS' : code[3]} )


if __name__ == "__main__":
	app.run(debug=True)

