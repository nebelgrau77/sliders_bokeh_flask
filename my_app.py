import os
import sqlite3 as sqlite
import pandas as pd

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

from bokeh_sliders import sliders_chart, better_sliders_chart

from dataframes import dataframe, assign_points, assign_cyl_points, dataframe_points
from parameters import thresholds
from helpers import explanation

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
data = assign_points(data, 'horsepower', thresholds['horsepower'], reverse=True)
data = assign_points(data, 'acceleration', thresholds['acceleration'])
data = assign_points(data, 'weight_kg', thresholds['weight_kg'])
data = assign_points(data, 'liters_per_100km', thresholds['liters_per_100km'])
data = assign_cyl_points(data)

@app.route('/mpg_sliders')
def mpgsliders():

	'''get mean values of points from the precalculated pandas dataframe: 
	this requires querying the whole database into a pandas df and running the calculations;
	it means that the whole dataframe is in memory all the time; makes it easier later as the points are already calculated'''

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
							year = year, 
							explanation = explanation)
						


@app.route('/better_sliders')
def bettersliders():
	
	'''get mean values of points from the precalculated pandas dataframe: 
	this requires querying the whole database into a pandas df and running the calculations;
	it means that the whole dataframe is in memory all the time; makes it easier later as the points are already calculated'''
	
	model_years = [item[0] for item in db.session.query(Car.model_year.distinct()).all()]
	origins = [item[0] for item in db.session.query(Car.origin.distinct()).all()]

	year = request.args.get('year')
	origin = request.args.get('origin')
		
	if year and origin:
		year, origin = int(year), origin
	else:
		year, origin = 1977, 'EUROPE'

	query = db.session.query(func.avg(Car.horsepower), 
							func.avg(Car.acceleration), 							
							func.avg(Car.weight_kg),
							func.avg(Car.liters_per_100km)).filter(and_(Car.origin == origin, Car.model_year==year)).all()

	query = list(query[0])

	script, div, js_resources, css_resources = better_sliders_chart(query) # needs to be modified

	return render_template('bokeh_raw_sliders.html', 
							plot_script = script,
							plot_div = div,
							js_resources = js_resources,
							css_resources=css_resources,
							years = model_years,
							origins = origins,
							query = query,
							origin = origin,
							year = year,
							explanation=explanation)
	
	
