from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool, CustomJS
from bokeh.layouts import row, column, gridplot
from bokeh.io import curdoc

from helpers import get_color, score_calc, colors

def make_scatter(val):
	'''make a simple square chart'''
	
	datasource = ColumnDataSource(data = dict(x=[val], y = [val]))

	x_range, y_range = 10

	fig = figure(title=None, plot_width=400, plot_height=400,x_range = x_range, y_range = y_range, toolbar_location=None)	
	
	fig.scatter(x='x', y='y', source = datasource)
	
	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None
	
	'''
	callback = CustomJS(args=dict(source=actual_source), code="""
        var data = source.data;
        var f = cb_obj.value        
		var s = data['side']
		s = f
		source.change.emit();
    """)

	test_slider = Slider(start = 0, end = 5, value = 1, step = 1, title = 'Slider')

	test_slider.js_on_change('value', callback)

	'''
	
	layout = row(fig)
	
	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources
