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
	
	valueA = int(request.args.get('valueA'))
	valueB = int(request.args.get('valueB'))
	
	if valueA and valueB:
		value = valueA*valueB
	else:
		value = 0
	
	return render_template('sliders.html', value=value)
