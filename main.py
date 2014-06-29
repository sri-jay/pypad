from flask import Flask, render_template, request, jsonify, make_response
from subprocess import Popen, PIPE, STDOUT
import os
import random

app = Flask(__name__, static_url_path = "")

@app.route("/")
def hello():
	data = random.random()
	return render_template('main.html')

@app.route("/run",methods=['POST'])
def run_code():
	#check the request method
	if request.method == 'POST':
		code = request.form['code']

		print code
		#write code to file
		os.chdir("/app/")
		temp = open("temp.py","w")
		temp.write(code)
		temp.close()

		#run the code 
		#stdout and std err are [0] and [1] in pipe
		input_pipe = Popen('python temp.py',stdout=PIPE,stderr=PIPE,shell=False)

		#fetch stdout
		program_output, program_error = input_pipe.communicate()

		print program_output
		print program_error

		program_output = "STDOUT :\n"+program_output+'\n\n'
		program_error = "STDERR :\n"+program_error+'\n\n'

		return jsonify( {'STDOUT' : program_output,'STDERR' : program_error})


if __name__ == "__main__":
	app.run()

