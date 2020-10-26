colors = {'white': '#ffffff', 'gray': '#888888', 'red': '#E8898E', 'yellow': '#ECBA91', 'green': '#9BC4AF'}
weights = {'hp': 0.2, 'accel': 0.3, 'weight': 0.1, 'mpg': 0.4}
quality_weight, price_weight = 0.7, 0.3	

def get_color(value):
	if value > 10:
		color = colors['gray']
	elif value > 8:
		color = colors['green']
	elif value > 4:
		color = colors['yellow']
	else:
		color = colors['red']		
	return color

def score_calc(points):
	score = points[0]*quality_weight + points[1]*price_weight
	return score
	
def score_calc_sliders(points, weights):
	weights = list(weights.values())
	score = sum([point*weight for point,weight in zip(points, weights)])
	return score

def js_formatter(js_master, value, weights):
	'''formats a JS code string with appropriate parameters'''
	values = list(weights.keys())
	values.remove(value)
	js_string = js_master % (value, weights[value], values[0], weights[values[0]], values[1], weights[values[1]], values[2], weights[values[2]], colors['red'], colors['yellow'], colors['green'])
	return js_string