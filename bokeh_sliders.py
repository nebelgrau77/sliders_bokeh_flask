from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool, CustomJS
from bokeh.layouts import row, column, gridplot

from helpers import get_color, score_calc, score_calc_sliders, js_formatter, js_formatter_raw, js_formatter_better
from parameters import colors, weights, thresholds
from jscode import jscode_master1, jscode_master2, jscode_bday

from birthday import scaler, birthdaycolor

def sliders_chart(query):
	'''make a simple square chart'''

	score = score_calc_sliders(query, weights)

	x_range = (0,9)
	y_range = (0,5)

	coords = ([2],[3])
	label = '{:.1f}'.format(score)
	color = get_color(score)

	side = 4

	datasource = ColumnDataSource(data = dict(x=coords[0], y=coords[1], hp = [query[0]], accel = [query[1]], weight = [query[2]], mpg = [query[3]], color = [color], label = [label], side = [side]))

	fig = figure(title=None, plot_width=480, plot_height=280,x_range = x_range, y_range = y_range, toolbar_location=None)

	fig.rect(x='x',y='y',width = 'side', height = 'side',fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = datasource)
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_font_size = "48px", text_align='center', text_baseline="middle", source = datasource)
	fig.text(x=0, y=1, text=['simulation'], text_font_style="bold", text_font_size = "20px", text_align='left', text_baseline="top")

	fig.rect(x=7,y=3,width = 'side', height = 'side',fill_color = color, fill_alpha = 0.8, line_color = colors['white'], source = datasource)
	fig.text(x=7, y=3, text=[label], text_font_style="bold", text_font_size = "48px", text_align='center', text_baseline="middle")
	fig.text(x=5, y=1, text=['original'], text_font_style="bold", text_font_size = "20px", text_align='left', text_baseline="top")

	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None

	jscode0 = js_formatter(jscode_master1, 'hp', weights)
	jscode1 = js_formatter(jscode_master1, 'accel', weights)
	jscode2 = js_formatter(jscode_master1, 'weight', weights)
	jscode3 = js_formatter(jscode_master1, 'mpg', weights)

	# the starting values should be those of the query

	slider_hp = CustomJS(args = dict(source = datasource), code = jscode0)
	score_hp = Slider(start = 1, end = 5, value = query[0], step = .1, title = 'Engine power', format = "0.0")
	score_hp.js_on_change('value', slider_hp)

	slider_accel = CustomJS(args = dict(source = datasource), code = jscode1)
	score_accel = Slider(start = 1, end = 5, value = query[1], step = .1, title = 'Acceleration', format = "0.0")
	score_accel.js_on_change('value', slider_accel)

	slider_weight = CustomJS(args = dict(source = datasource), code = jscode2)
	score_weight = Slider(start = 1, end = 5, value = query[2], step = .1, title = 'Weight', format = "0.0")
	score_weight.js_on_change('value', slider_weight)

	slider_mpg = CustomJS(args = dict(source = datasource), code = jscode3)
	score_mpg = Slider(start = 1, end = 5, value = query[3], step = .1, title = 'Fuel consumption', format = "0.0")
	score_mpg.js_on_change('value', slider_mpg)

	sliders = column(score_mpg, score_accel, score_hp, score_weight)
	layout = row(sliders, fig)

	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources


def better_sliders_chart(query):
	
	'''make a square chart using raw query results'''

	'''the score has to be calculated just like it is in the dataframe, but on single scalar values'''

	#score = score_calc_sliders(query, weights) # this needs to be replaced with a new function

	score = 3

	x_range = (0,9)
	y_range = (0,5)

	coords = ([2],[3])
	label = '{:.1f}'.format(score)
	color = get_color(score)

	side = 4

	datasource = ColumnDataSource(data = dict(x=coords[0], y=coords[1], hp = [query[0]], accel = [query[1]], weight = [query[2]], mpg = [query[3]], color = [color], label = [label], side = [side]))

	fig = figure(title=None, plot_width=480, plot_height=280,x_range = x_range, y_range = y_range, toolbar_location=None)

	fig.rect(x='x',y='y',width = 'side', height = 'side',fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = datasource)
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_font_size = "48px", text_align='center', text_baseline="middle", source = datasource)
	fig.text(x=0, y=1, text=['simulation'], text_font_style="bold", text_font_size = "20px", text_align='left', text_baseline="top")

	fig.rect(x=7,y=3,width = 'side', height = 'side',fill_color = color, fill_alpha = 0.8, line_color = colors['white'], source = datasource)
	fig.text(x=7, y=3, text=[label], text_font_style="bold", text_font_size = "48px", text_align='center', text_baseline="middle")
	fig.text(x=5, y=1, text=['original'], text_font_style="bold", text_font_size = "20px", text_align='left', text_baseline="top")

	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None

	'''rewrite the JS code to accept the threshold values from Python code arguments; ideally use f-strings for clarity'''

	jscode0 = js_formatter_better(jscode_master2, 'hp', weights, colors, thresholds)
	jscode1 = js_formatter_better(jscode_master2, 'accel', weights, colors, thresholds)	
	jscode2 = js_formatter_better(jscode_master2, 'weight', weights, colors, thresholds)	
	jscode3 = js_formatter_better(jscode_master2, 'mpg', weights, colors, thresholds)	

	# the start/end values and steps have to be adjusted to reflect the parameters, e.g. horsepower 50 - 300 etc.

	slider_hp = CustomJS(args = dict(source = datasource), code = jscode0)

	score_hp = Slider(start = 30, end = 300, value = query[0], step = 5, title = 'Engine power [HP]', format = "0")
	score_hp.js_on_change('value', slider_hp)

	slider_accel = CustomJS(args = dict(source = datasource), code = jscode1)
	score_accel = Slider(start = 5, end = 30, value = query[1], step = .1, title = 'Acceleration 0-96 km/h [s]', format = "0.0")
	score_accel.js_on_change('value', slider_accel)

	slider_weight = CustomJS(args = dict(source = datasource), code = jscode2)
	score_weight = Slider(start = 500, end = 2500, value = query[2], step = 25, title = 'Weight [kg]', format = "0")
	score_weight.js_on_change('value', slider_weight)

	slider_mpg = CustomJS(args = dict(source = datasource), code = jscode3)
	score_mpg = Slider(start = 5, end = 30, value = query[3], step = .1, title = 'Fuel consumption [l/100km]', format = "0.0")

	score_mpg.js_on_change('value', slider_mpg)

	sliders = column(score_mpg, score_accel, score_hp, score_weight)
	layout = row(sliders, fig)

	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources


def birthday_sliders():

	#year, month, day = birthdate # birthdate is a tuple (YY,MM,DD)

	x_range = (0,4)
	y_range = (0,4)

	coords = ([2],[2])
	
	bday_year = 70
	bday_month = 1
	bday_day = 1

	

	color = birthdaycolor('700101') # replace with a simple hex value, remove the calc function

	side = 4

	label = '70/01/01'

	datasource = ColumnDataSource(data = dict(x=coords[0], y=coords[1], year = [bday_year], month = [bday_month], day = [bday_day], color = [color], label = [label], side = [side]))

	fig = figure(title=None, plot_width=400, plot_height=400,x_range = x_range, y_range = y_range, toolbar_location=None)
	fig.rect(x='x',y='y',width = 'side', height = 'side',fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = datasource)
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_font_size = "48px", text_align='center', text_baseline="middle", source = datasource)

	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None

	jscode_year = jscode_bday.format(slidervalue='year')
	jscode_month = jscode_bday.format(slidervalue='month')
	jscode_day = jscode_bday.format(slidervalue='day')


	change_year = CustomJS(args = dict(source = datasource), code = jscode_year)
	slider_year = Slider(start = 0, end = 99, value = 70, step = 1, title = 'Year', format = "00")
	slider_year.js_on_change('value', change_year)

	change_month = CustomJS(args = dict(source = datasource), code = jscode_month)
	slider_month = Slider(start = 1, end = 12, value = 1, step = 1, title = 'Month', format = "00")
	slider_month.js_on_change('value', change_month)

	change_day = CustomJS(args = dict(source = datasource), code = jscode_day)
	slider_day = Slider(start = 1, end = 31, value = 1, step = 1, title = 'Day', format = "00")
	slider_day.js_on_change('value', change_day)

	#sliders = column(slider_year, slider_month, slider_day)
	#layout = row(sliders, fig)
	layout = column(fig, slider_year, slider_month, slider_day)

	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources