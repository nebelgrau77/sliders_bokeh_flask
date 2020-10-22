from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.models import HoverTool
from helpers import get_color, score_calc

def simple_bokeh_chart(query):
	'''make a simple square chart'''
	
	score = score_calc(query)	
	score_color = get_color(score)
	
	test = (3,3)
	test_score = score_calc(test)
	test_color = get_color(test_score)
	
	xr = (0,9)
	yr = (0,4)

	fig = figure(title=None, plot_width=420, plot_height=200,x_range = xr, y_range = yr, toolbar_location=None)	
	
	xs = [2,7]
	ys = [2,2]
	labels = ['{:.1f}'.format(score), '{:.1f}'.format(test_score)]
	square_side = 4

	source = ColumnDataSource(dict(x=xs, y=ys, label=labels))
	
	fig.rect(xs[0],ys[0],square_side,square_side,fill_color = score_color, fill_alpha = 0.8, line_color = c_white)	# real values
	fig.rect(xs[1],ys[1],square_side,square_side,fill_color = test_color, fill_alpha = 0.8, line_color = c_white)	# test values
	
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
