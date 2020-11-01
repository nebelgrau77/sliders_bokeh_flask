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

def js_formatter_better(js_master, value, weights, colors, thresholds):
	'''formats a JS code string with appropriate parameters'''

	t3_hp, t2_hp, t1_hp, t0_hp = list(thresholds['horsepower'].keys())
	t3_accel, t2_accel, t1_accel, t0_accel = list(thresholds['acceleration'].keys())
	t3_kg, t2_kg, t1_kg, t0_kg = list(thresholds['weight_kg'].keys())
	t3_mpg, t2_mpg, t1_mpg, t0_mpg = list(thresholds['liters_per_100km'].keys())

	js_string = js_master.format(slider_value=value, 
								hp_thresh_3 = t3_hp,
								hp_thresh_2 = t2_hp,
								hp_thresh_1 = t1_hp,
								hp_thresh_0 = t0_hp,
								accel_thresh_3 = t3_accel, 
								accel_thresh_2 = t2_accel,
								accel_thresh_1 = t1_accel,
								accel_thresh_0 = t0_accel,
								weight_thresh_3 = t3_kg,
								weight_thresh_2 = t2_kg,
								weight_thresh_1 = t1_kg,
								weight_thresh_0 = t0_kg,
								mpg_thresh_3 = t3_mpg,
								mpg_thresh_2 = t2_mpg,
								mpg_thresh_1 = t1_mpg,
								mpg_thresh_0 = t0_mpg,
								hp_weight = weights['hp'],
								accel_weight = weights['accel'],
								weight_weight = weights['weight'],
								mpg_weight = weights['mpg'],
								red = colors['red'],
								yellow = colors['yellow'],
								green = colors['green'],
								)

	return js_string

explanation = '''Move the sliders to simulate the overall score change.

The squares show a score calculated with four parameters: fuel consumption, acceleration, weight and horsepower.
The overall score is a weighted average, with the following weigths:
 - fuel consumption 40%, 
 - acceleration 30%, 
 - horsepower 20% 
 - weight 10%.
The lower the parameter, the higher the score (except for the horsepower).
Scores over 4.0 are good (green color), below 3.0 bad (red color),between 3.0 and 4.0 medium (yellow).
'''
