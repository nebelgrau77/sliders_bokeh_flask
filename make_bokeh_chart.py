from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.models import HoverTool

def simple_bokeh_chart():
	'''make a simple square chart'''

	# chart defaults
	c_red = '#E8898E' 
	c_yellow = '#ECBA91'
	c_green = '#9BC4AF'
	c_white = '#ffffff'

	sample_text = ["text"]

	xr = (0,9)
	yr = (0,4)

	fig = figure(title=None, plot_width=420, plot_height=200,x_range = xr, y_range = yr, toolbar_location=None)	
	
	xs = [2,7]
	ys = [2,2]
	labels = ['', '']
	square_side = 4

	source = ColumnDataSource(dict(x=xs, y=ys, label=labels))
	
	fig.rect(xs[0],ys[0],square_side,square_side,fill_color = c_red, fill_alpha = 0.8, line_color = c_white)	
	fig.rect(xs[1],ys[1],square_side,square_side,fill_color = c_yellow, fill_alpha = 0.8, line_color = c_white)
	
	
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_align='left', text_baseline="middle", source = source)

	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None

	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(fig)

	return script, div, js_resources, css_resources
