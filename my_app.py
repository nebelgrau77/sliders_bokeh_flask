import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

# define paths to project and database
project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

bootstrap = Bootstrap(app) # initialize Bootstrap


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/sliders')
def sliders():
	
	valueA = request.args.get('valueA')
	valueB = request.args.get('valueB')	
	
	if valueA and valueB:
		value = int(valueA)*int(valueB)
	else:
		value = 0
	
	return render_template('sliders.html', value=value)

@app.route('/bokehtest')
def bokehtest():

	value = 77
	
	return render_template('bokehtest.html', value = value)