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