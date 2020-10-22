from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool
from bokeh.layouts import row, column, gridplot
from bokeh.io import curdoc

from helpers import get_color, score_calc, colors

def simple_bokeh_chart(query):
	'''make a simple square chart'''
	
	score = score_calc(query)	
	score_color = get_color(score)
	
	test = (3,3)
	
	xr = (0,9)
	yr = (0,4)
	
	xs = [2,7]
	ys = [2,2]	
	square_side = 4

	fig = figure(title=None, plot_width=420, plot_height=200,x_range = xr, y_range = yr, toolbar_location=None)	

	QS, PS = query
	
	slider_quality = Slider(start = 1, end = 10, value = QS, step = 1, title = 'Quality')
	slider_price = Slider(start = 1, end = 10, value = PS, step = 1, title = 'Price')

	test_score = score_calc((QS, PS))
	test_color = get_color(test_score)
	
	labels = ['{:.1f}'.format(score), '{:.1f}'.format(QS*2)]
	
	source = ColumnDataSource(dict(x=xs, y=ys, label=labels))
	
	fig.rect(xs[0],ys[0],square_side,square_side,fill_color = score_color, fill_alpha = 0.8, line_color = colors['white'])	# real values
	fig.rect(xs[1],ys[1],square_side,square_side,fill_color = test_color, fill_alpha = 0.8, line_color = colors['white'])	# test values
	
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_align='left', text_baseline="middle", source = source)

	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None

	
	# NOT WORKING YET
	
	def callback_quality(attr, old, new):
		QS = slider_quality.value				
	slider_quality.on_change('value', callback_quality)
	
	def callback_price(attr, old, new):
		PS = slider_price.value				
	slider_price.on_change('value', callback_price)
	
	# layout = gridplot([[slider_quality, fig], [slider_price, None]])
	
	sliders = column(slider_quality, slider_price)
	layout = row(sliders, fig)
	
	curdoc().add_root(layout)
	
	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources
