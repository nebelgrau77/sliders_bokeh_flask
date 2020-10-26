import os
import sqlite3 as sqlite
import pandas as pd

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from bokeh.embed import server_session
from bokeh.client import pull_session

from make_bokeh_chart import simple_bokeh_chart

from bokehtest import bokeh_test
from scatter import make_scatter
from bokeh_sliders import sliders

from dataframes import points, dataframe, assign_points, assign_cyl_points


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
	
	#testquery = db.session.query(Product.quality_score, Product.price_score).filter(Product.index==1).one()

	testquery = (6,7,4)

	script, div, js_resources, css_resources = simple_bokeh_chart(testquery)

	return render_template('bokeh_test.html',plot_script = script,plot_div = div,js_resources = js_resources,css_resources=css_resources,value=testquery)
	
@app.route('/bokehserver')
def bkapp():
	
	testquery = (2,6)

	script, div, js_resources, css_resources = bokeh_test()

	return render_template('bokeh_test.html',plot_script = script,plot_div = div,js_resources = js_resources,css_resources=css_resources,value=testquery)


@app.route('/scatter')
def test_scatter():
	
	val = 5

	script, div, js_resources, css_resources = make_scatter(val)

	return render_template('bokeh_test.html',plot_script = script,plot_div = div,js_resources = js_resources,css_resources=css_resources,value=val)

cars_database = os.path.join(project_dir,'data/cars.db')

data = dataframe(cars_database, 'cars')
data = assign_points(data, 'horsepower', points['horsepower'], reverse=True)
data = assign_points(data, 'acceleration', points['acceleration'])
data = assign_points(data, 'weight_kg', points['weight_kg'])
data = assign_points(data, 'liters_per_100km', points['liters_per_100km'])
data = assign_cyl_points(data)

model_years = list(data['model_year'].unique())
origins = list(data['origin'].unique())

@app.route('/mpg_sliders')
def mpgsliders():

	# get mean values of the points for modelyear/origin chosen by the user: ['horsepower','accel', 'weight_kg', 'liters_per_100km', 'cylinders']

	year = request.args.get('year')
	origin = request.args.get('origin')

	query = data.loc[(data['model_year'] == year) & (data['origin'] == origin), 
					['horsepower_points', 'acceleration_points', 'weight_kg_points', 'liters_per_100km_points', 'cylinders_points']].mean()
	
	query = list(query)

	# script, div, js_resources, css_resources = sliders(query) - needs to be modified

	return render_template('bokeh_sliders.html', years = model_years, origins = origins, query = query)