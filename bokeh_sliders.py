from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool, CustomJS
from bokeh.layouts import row, column, gridplot
from bokeh.io import curdoc

from helpers import get_color, score_calc, score_calc_sliders, js_formatter, js_formatter_raw, js_formatter_better
from parameters import colors, weights, thresholds

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


	jscode_master = """
        var data = source.data;
		var v = cb_obj.value

		var hp = data['hp']
		var accel = data['accel']
		var weight = data['weight']
		var mpg = data['mpg']

		var label = data['label']
		var color = data['color']

		%s[0] = v

		var score =  v * %s + %s * %s + %s * %s + %s * %s

		label[0] = score.toFixed(1)

		
		if (score < 3) {
			color[0]  = '%s'
		}
		else if (score < 4) {
			color[0]  = '%s'
		}
		else {
			color[0]  = '%s'
		}
		

		source.change.emit();
    """


	jscode0 = js_formatter(jscode_master, 'hp', weights)
	jscode1 = js_formatter(jscode_master, 'accel', weights)
	jscode2 = js_formatter(jscode_master, 'weight', weights)
	jscode3 = js_formatter(jscode_master, 'mpg', weights)

	# the starting values should be those of the query

	slider_hp = CustomJS(args = dict(source = datasource), code = jscode0)
	score_hp = Slider(start = 1, end = 5, value = query[0], step = .1, title = 'Engine power [HP]', format = "0.0")
	score_hp.js_on_change('value', slider_hp)

	slider_accel = CustomJS(args = dict(source = datasource), code = jscode1)
	score_accel = Slider(start = 1, end = 5, value = query[1], step = .1, title = 'Acceleration 0-96 km/h [s]', format = "0.0")
	score_accel.js_on_change('value', slider_accel)

	slider_weight = CustomJS(args = dict(source = datasource), code = jscode2)
	score_weight = Slider(start = 1, end = 5, value = query[2], step = .1, title = 'Weight [kg]', format = "0.0")
	score_weight.js_on_change('value', slider_weight)

	slider_mpg = CustomJS(args = dict(source = datasource), code = jscode3)
	score_mpg = Slider(start = 1, end = 5, value = query[3], step = .1, title = 'Fuel onsumption [l/100km]', format = "0.0")
	score_mpg.js_on_change('value', slider_mpg)

	sliders = column(score_mpg, score_accel, score_hp, score_weight)
	layout = row(sliders, fig)

	#curdoc().add_root(layout) # not sure if that's even necessary

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
	

	jscode_master = """
        var data = source.data;
		var v = cb_obj.value

		var hp = data['hp']
		var accel = data['accel']
		var weight = data['weight']
		var mpg = data['mpg']

		var label = data['label']
		var color = data['color']

		{slider_value}[0] = v //this is the value that is updated by this slider

		var hp_points = 0
		var accel_points = 0
		var weight_points = 0
		var mpg_points = 0
		
		if (hp > {hp_thresh_3}) {{
			hp_points = 5
		}}
		else if (hp > {hp_thresh_2}) {{
			hp_points = 4
		}}
		else if (hp > {hp_thresh_1}) {{
			hp_points = 3
		}}
		else if (hp > {hp_thresh_0}) {{
			hp_points = 2
		}}
		else {{
			hp_points = 1
		}}

		if (accel < {accel_thresh_3}) {{
			accel_points = 5
		}}
		else if (accel < {accel_thresh_2}) {{
			accel_points = 4
		}}
		else if (accel < {accel_thresh_1}) {{
			accel_points = 3
		}}
		else if (accel < {accel_thresh_0}) {{
			accel_points = 2
		}}
		else {{
			accel_points = 1
		}}

		if (weight < {weight_thresh_3}) {{
			weight_points = 5
		}}
		else if (weight < {weight_thresh_2}) {{
			weight_points = 4
		}}
		else if (weight < {weight_thresh_1}) {{
			weight_points = 3
		}}
		else if (weight < {weight_thresh_0}) {{
			weight_points = 2
		}}
		else {{
			weight_points = 1
		}}

		if (mpg < {mpg_thresh_3}) {{
			mpg_points = 5
		}}
		else if (mpg < {mpg_thresh_2}) {{
			mpg_points = 4
		}}
		else if (mpg < {mpg_thresh_1}) {{
			mpg_points = 3
		}}
		else if (mpg < {mpg_thresh_0}) {{
			mpg_points = 2
		}}
		else {{
			mpg_points = 1
		}}

		var score = hp_points * {hp_weight} + accel_points * {accel_weight} + weight_points * {weight_weight} + mpg_points * {mpg_weight}

		label[0] = score.toFixed(1) 

		if (score < 3) {{
			color[0]  = '{red}'
		}}
		else if (score < 4) {{
			color[0]  = '{yellow}'
		}}
		else {{
			color[0]  = '{green}'
		}}

		source.change.emit();
    """


	jscode0 = js_formatter_better(jscode_master, 'hp', weights, colors, thresholds)
	print(jscode0)
	jscode1 = js_formatter_better(jscode_master, 'accel', weights, colors, thresholds)	
	jscode2 = js_formatter_better(jscode_master, 'weight', weights, colors, thresholds)	
	jscode3 = js_formatter_better(jscode_master, 'mpg', weights, colors, thresholds)
	

	# the start/end values and steps have to be adjusted to reflect the parameters, e.g. horsepower 50 - 300 etc.

	slider_hp = CustomJS(args = dict(source = datasource), code = jscode0)
	score_hp = Slider(start = 30, end = 300, value = query[0], step = 5, title = 'Engine power [HP]', format = "0")
	score_hp.js_on_change('value', slider_hp)

	slider_accel = CustomJS(args = dict(source = datasource), code = jscode1)
	score_accel = Slider(start = 5, end = 30, value = query[1], step = .5, title = 'Acceleration 0-96 km/h [s]', format = "0.0")
	score_accel.js_on_change('value', slider_accel)

	slider_weight = CustomJS(args = dict(source = datasource), code = jscode2)
	score_weight = Slider(start = 500, end = 2500, value = query[2], step = 25, title = 'Weight [kg]', format = "0")
	score_weight.js_on_change('value', slider_weight)

	slider_mpg = CustomJS(args = dict(source = datasource), code = jscode3)
	score_mpg = Slider(start = 5, end = 30, value = query[3], step = .1, title = 'Fuel consumption [l/100km]', format = "0.0")
	score_mpg.js_on_change('value', slider_mpg)

	sliders = column(score_mpg, score_accel, score_hp, score_weight)
	layout = row(sliders, fig)

	#curdoc().add_root(layout) # not sure if that's even necessary

	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources