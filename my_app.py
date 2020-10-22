import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from make_bokeh_chart import simple_bokeh_chart

# define paths to project and database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'sqlite:///{}'.format(os.path.join(project_dir, 'products.db'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file # tell the app where the database is

bootstrap = Bootstrap(app) # initialize Bootstrap

db = SQLAlchemy(app) # initialize a connection to the database

class Product(db.Model):
	__tablename__ = 'products'
	index = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
	category = db.Column(db.String(40), unique = False, nullable=False) # e.g. TV, radio...
	brand = db.Column(db.String(40), unique = False, nullable=False)
	quality_score = db.Column(db.Integer, unique = False, nullable=True)
	price_score = db.Column(db.Integer, unique = False, nullable=True)

	def __repr__(self):
		return "<Index: {:05d}, Category: {}, Brand: {}, Quality score: {}, Price score: {}".format(self.index, self.category, self.brand, self.quality_score,self.price_score)



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
	
	
	
