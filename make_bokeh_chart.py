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

	fig = figure(title='Test', plot_width=500, plot_height=500,toolbar_location=None)	

	xs = [1,1,3,3]
	ys = [1,3,1,3]
	labels = ['SW', 'NW', 'SE', 'NE']

	source = ColumnDataSource(dict(x=xs, y=ys, label=labels))

	
	fig.rect(1,1, 2,2, fill_color = c_red, fill_alpha = 0.8, line_color = c_white)
	fig.rect(1,3, 2,2, fill_color = c_yellow, fill_alpha = 0.8, line_color = c_white)
	fig.rect(3,1, 2,2, fill_color = c_yellow, fill_alpha = 0.8, line_color = c_white)
	fig.rect(3,3, 2,2, fill_color = c_green, fill_alpha = 0.8, line_color = c_white)
	
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
