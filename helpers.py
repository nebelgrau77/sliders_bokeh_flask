colors = {'white': '#ffffff', 'gray': '#888888', 'red': '#E8898E', 'yellow': '#ECBA91', 'green': '#9BC4AF'}

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
	
quality_weight = 0.7
price_weight = 0.3	

def score_calc(points):
	score = points[0]*quality_weight + points[1]*price_weight
	return score
	
	