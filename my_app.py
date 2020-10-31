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
from bokeh_sliders import sliders_chart

from sqlalchemy import func

from helpers import explanation
from dataframes import points, dataframe, assign_points, assign_cyl_points, dataframe_points


# define paths to project and database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'sqlite:///{}'.format(os.path.join(project_dir, 'data/cars.db'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file # tell the app where the database is

bootstrap = Bootstrap(app) # initialize Bootstrap

db = SQLAlchemy(app) # initialize a connection to the database

class Car(db.Model):
    __tablename__ = 'cars'
    index = db.Column(db.Integer(), unique = True, nullable=False, primary_key=True)
    brand = db.Column(db.String(40), unique = False, nullable = False)
    model = db.Column(db.String(40), unique = False, nullable = True)
    model_year = db.Column(db.Integer(), unique = False, nullable=False)
    origin = db.Column(db.String(80), unique = False, nullable = True)
    cylinders = db.Column(db.Integer(), unique = False, nullable=False)
    displacement_ccm = db.Column(db.Float(), unique = False, nullable=False)
    horsepower = db.Column(db.Integer(), unique = False, nullable=False)
    acceleration = db.Column(db.Float(), unique = False, nullable=False)
    weight_kg = db.Column(db.Float(), unique = False, nullable=False)
    liters_per_100km = db.Column(db.Float(), unique = False, nullable=False)

    def __repr__(self):
        return "<Brand: {}, Model: {}, Origin: {}>".format(self.brand, self.model, self.origin)

@app.route('/')
def home():
	return render_template('home.html')

cars_database = os.path.join(project_dir,'data/cars.db')

data = dataframe(cars_database, 'cars')
data = assign_points(data, 'horsepower', points['horsepower'], reverse=True)
data = assign_points(data, 'acceleration', points['acceleration'])
data = assign_points(data, 'weight_kg', points['weight_kg'])
data = assign_points(data, 'liters_per_100km', points['liters_per_100km'])
data = assign_cyl_points(data)


@app.route('/mpg_sliders')
def mpgsliders():
	
	model_years = list(data['model_year'].unique())
	origins = list(data['origin'].unique())

	# get mean values of the points for modelyear/origin chosen by the user: ['horsepower','accel', 'weight_kg', 'liters_per_100km', 'cylinders']

	year = request.args.get('year')
	origin = request.args.get('origin')
		
	if year and origin:
		year, origin = int(year), origin
	else:
		year, origin = 1977, 'EUROPE'
	
	query = data.loc[(data['model_year'] == year) & (data['origin'] == origin), 
					['horsepower_points', 'acceleration_points', 'weight_kg_points', 'liters_per_100km_points']].mean()
			
	query = list(query)
		
	script, div, js_resources, css_resources = sliders_chart(query) # needs to be modified

	return render_template('bokeh_sliders.html', 
							plot_script = script,
							plot_div = div,
							js_resources = js_resources,
							css_resources=css_resources,
							years = model_years,
							origins = origins,
							query = query,
							origin = origin,
							year = year)
							


@app.route('/better_sliders')
def bettersliders():
	
	pass

	
	# myquery = db.session.query(Car.model_year, func.avg(queries.get(val, Car.weight_kg))).group_by(Car.model_year).all()

	model_years = [item[0] for item in db.session.query(Car.model_year.distinct()).all()]
	origins = [item[0] for item in db.session.query(Car.origin.distinct()).all()]

	year = request.args.get('year')
	origin = request.args.get('origin')
		
	if year and origin:
		year, origin = int(year), origin
	else:
		year, origin = 1977, 'EUROPE'

	myquery = db.session.query(func.avg(Car.horsepower), 
							func.avg(Car.acceleration), 							
							func.avg(Car.weight_kg),
							func.avg(Car.liters_per_100km)).filter(Car.origin == origin).all()

	'''

	# get mean values of the points for modelyear/origin chosen by the user: ['horsepower','accel', 'weight_kg', 'liters_per_100km', 'cylinders']

	query = db.session.query(Product.quality_score, Product.price_score).filter(Product.index==1).one()

	
	
	query = data.loc[(data['model_year'] == year) & (data['origin'] == origin), 
					['horsepower_points', 'acceleration_points', 'weight_kg_points', 'liters_per_100km_points']].mean()
			
	query = list(query)
		
	script, div, js_resources, css_resources = sliders_chart(query) # needs to be modified

	return render_template('bokeh_sliders.html', 
							plot_script = script,
							plot_div = div,
							js_resources = js_resources,
							css_resources=css_resources,
							years = model_years,
							origins = origins,
							query = query,
							origin = origin,
							year = year)
	
	'''

	return render_template('test_select.html', model_years = model_years, origins=origins, query = myquery, origin = origin.title())