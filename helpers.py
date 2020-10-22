def get_color(value):
	if value > 10:
		color = '#888888' # gray
	elif value > 8:
		color = '#9BC4AF' # green
	elif value > 4:
		color = '#ECBA91' # yellow
	else:
		color = '#E8898E' # red
		
	return color


quality_weight = 0.7
price_weight = 0.3	

def score_calc(points):
	score = points[0]*quality_weight + points[1]*price_weight
	return score
	
	