from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, HoverTool
from bokeh.layouts import row, column, gridplot
from bokeh.io import curdoc

from helpers import get_color, score_calc, colors


query = (5,8)

actual_score = score_calc(query)	

	
test = (3,3)

x_range = (0,9)
y_range = (0,4)
	
	
# SEEMS TO REQUIRE BOKEH SERVER INSTEAD TO WORK WITH CALLBACKS
	
	
actual_coords = ([2],[2])
actual_label = '{:.1f}'.format(actual_score)
actual_color = get_color(actual_score)
	
actual_source = ColumnDataSource(data = dict(x=actual_coords[0], y=actual_coords[1], label = [actual_label], color = [actual_color]))
		
square_side = 4

fig = figure(title=None, plot_width=420, plot_height=200,x_range = x_range, y_range = y_range, toolbar_location=None)	

QS, PS = query
	
quality_score = Slider(start = 1, end = 10, value = QS, step = 1, title = 'Quality')
price_score = Slider(start = 1, end = 10, value = PS, step = 1, title = 'Price')

test_score = score_calc((QS, PS))
test_color = get_color(test_score)
	
test_coords = ([7],[2])
test_source = ColumnDataSource(data = dict(x=test_coords[0], y=test_coords[1], label = ['{:.1f}'.format(test_score)], color = [test_color]))
	
fig.rect(x='x',y='y',width = square_side, height = square_side,fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = actual_source)	# real values
fig.text(x='x', y='y', text='label', text_font_style="bold", text_align='left', text_baseline="middle", source = actual_source)
	
fig.rect(x='x',y='y',width = square_side, height = square_side,fill_color = 'color', fill_alpha = 0.8, line_color = colors['white'], source = test_source)	# test values
fig.text(x='x', y='y', text='label', text_font_style="bold", text_align='left', text_baseline="middle", source = test_source)
		
fig.outline_line_color = None
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.minor_tick_line_color = None
fig.axis.major_label_text_color = None

	
def update(attrname, old, new):
		
	# get the current slider values
		
	qs = quality_score.value
	ps = price_score.value
		
	# update the test score calculation
		
	testscore = score_calc((qs, ps))	
	testcolor = get_color(testscore)
	test_source.data = dict(x=test_coords[0], y=test_coords[1], label = ['{:.1f}'.format(testscore)], color = [testcolor])			
	
for param in [quality_score, price_score]:
	param.on_change('value', update)
	
sliders = column(quality_score, price_score)
layout = row(sliders, fig)
	
curdoc().add_root(layout) # not sure if that's even necessary
	
