from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool, CustomJS
from bokeh.layouts import row, column, gridplot
from bokeh.io import curdoc

from helpers import get_color, score_calc, colors

### IDEA: have the query values in the data source. in each slider callback extract the OTHER value (e.g. in price callback get the quality value from the source, and the
# price value from the slider). update the value corresponding to the slider (so it's ready for the other slider), and whatever value has to be calculated, e.g. total score



def simple_bokeh_chart(query):
	'''make a simple square chart'''
	
	score = score_calc(query)	
	
	x_range = (0,4)
	y_range = (0,4)
		
	coords = ([2],[2])
	label = '{:.1f}'.format(score)
	color = get_color(score)
	
	side = 4

	datasource = ColumnDataSource(data = dict(x=coords[0], y=coords[1], price = [query[0]], quality = [query[1]], color = [color], label = [label], side = [side]))

	fig = figure(title=None, plot_width=200, plot_height=200,x_range = x_range, y_range = y_range, toolbar_location=None)	

	fig.rect(x='x',y='y',width = 'side', height = 'side',fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = datasource)	# test values
	fig.text(x='x', y='y', text='label', text_font_style="bold", text_align='left', text_baseline="middle", source = datasource)
	
	fig.outline_line_color = None
	fig.grid.grid_line_color = None
	fig.axis.axis_line_color = None
	fig.axis.major_tick_line_color = None
	fig.axis.minor_tick_line_color = None
	fig.axis.major_label_text_color = None
	
	jscode1 = """
        var data = source.data;
        var v = cb_obj.value	
		var price = data['price']
		var label = data['label']
		var score = price * 0.3 + v * 0.7

		label[0] = score.toFixed(1)

		var color = data['color']

		if (score < 4) {
			color[0]  = '#E8898E'
		}
		else if (score < 8) {
			color[0]  = '#ECBA91'
		}
		else {
			color[0]  = '#9BC4AF'
		}

		source.change.emit();
    """

	jscode2 = """
        var data = source.data;
        var v = cb_obj.value	
		var quality = data['quality']
		var label = data['label']
		var score = v * 0.3 + quality * 0.7

		label[0] = score.toFixed(1)

		var color = data['color']

		if (score < 4) {
			color[0]  = '#E8898E'
		}
		else if (score < 8) {
			color[0]  = '#ECBA91'
		}
		else {
			color[0]  = '#9BC4AF'
		}

		source.change.emit();
    """


	quality_changer = CustomJS(args = dict(source = datasource), code = jscode1)	
	quality_score = Slider(start = 1, end = 10, value = 5, step = 1, title = 'Quality')
	quality_score.js_on_change('value', quality_changer)

	price_changer = CustomJS(args = dict(source = datasource), code = jscode2)	
	price_score = Slider(start = 1, end = 10, value = 5, step = 1, title = 'Price')
	price_score.js_on_change('value', price_changer)
	
	
	sliders = column(quality_score, price_score)
	layout = row(sliders, fig)
	
	

	#curdoc().add_root(layout) # not sure if that's even necessary
	
	#grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	#get the resources from the figure components
	script, div = components(layout)

	return script, div, js_resources, css_resources
