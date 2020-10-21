import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from make_bokeh_chart import simple_bokeh_chart

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
	
	script, div, js_resources, css_resources = simple_bokeh_chart()

	return render_template('bokeh_test.html',plot_script = script,plot_div = div,js_resources = js_resources,css_resources=css_resources,value=value)
	
	
	
