from parameters import colors

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

def js_formatter_raw(js_master, value, weights):
	'''formats a JS code string with appropriate parameters'''
	js_string = js_master % (value, weights['hp'], weights['accel'], weights['weight'], weights['mpg'], colors['red'], colors['yellow'], colors['green'])
	return js_string

explanation = '''The squares show a score calculated based on four parameters: fuel consumption, acceleration, weight and horsepower. The lower the parameter, the higher the score (except for the horsepower).
The overall score is a weighted average, with the following weigths: fuel consumption 40%, acceleration 30%, horsepower 20% and weight 10%.
Scores over 4.0 are good (green color), below 3.0 bad (red color),between 3.0 and 4.0 medium (yellow).
Move the sliders to simulate the overall score change.'''
