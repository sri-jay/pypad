from flask import Flask, render_template, request, jsonify, make_response
from flask_mail import Mail,Message
from subprocess import Popen, PIPE, STDOUT
import os
import random
import hashlib
import psycopg2
import json
import urlparse

# Setup url parse to read DB login data as environment string
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

app = Flask(__name__, static_url_path = "")
app.config.update(dict(
	MAIL_SERVER = "smtp.gmail.com",
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = os.environ['EMAIL_USERNAME'],
	MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
))

app.config.from_object(__name__)



def connect_to_db():

	print "Creating connection object."
	db_connection = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
	)

	return db_connection

def send_mail(recipient,hash_code):
	mail = Mail(app)

	msg = Message("Your python snippet",sender="sriduth.jayhari@gmail.com",recipients=[recipient])
	msg.body = render_template("email.html",emailid=recipient.split('@')[0],link="http://pypad.herokuapp.com/get/"+hash_code)

	mail.send(msg)


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
		conn = connect_to_db()
		cursor = conn.cursor()

		query = """SELECT unique_hash,email FROM data"""

		print query

		cursor.execute(query)
		code = cursor.fetchall()

		print code

	except Exception as e:
		print e

	conn.close()
	return jsonify( {'hashes' : code} )

@app.route("/save",methods=['POST'])
def save_code():
	print "Saving code"
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
	send_mail(_email_,_unique_hash_)	
	print "\n"
	try:

		# Get connection object
		conn = connect_to_db()

		#get a cursor
		print "Writing to DB"
		cursor = conn.cursor()

		# create th query
		query =  """INSERT INTO data VALUES(\'%s\',\'%s\',\'%s\',\'%s\');"""%(_unique_hash_,_email_,_code_,_comments_)
		print query

		# Execute query
		cursor.execute(query)
		conn.commit()


	except Exception as e:
		print "DB operation faliled"
		print e
		STATUS = "FALSE"

	return jsonify({'STATUS' : STATUS})

@app.route("/get/<data>",methods=['GET','POST'])
def get_code(data):
	print "Here"
	code_hash = data
	print data
	try:
		conn = connect_to_db()

		cursor = conn.cursor()
		query = """SELECT * FROM data where unique_hash=\'%s\'"""%(code_hash)
		print query
		cursor.execute(query)
		code = cursor.fetchone()
		print code
	except Exception as e:
		print e


	#return jsonify( {'CODE' : code[2],'EMAIL' : code[1],'COMMENTS' : code[3]} )
	return render_template('view_code.html',comments=code[3],source=code[2].replace(',',' ,'),url=str(hashlib.sha224(str(random.random())).hexdigest()))

if __name__ == "__main__":
	app.run(debug=True)

