jscode_master1 = """
        var data = source.data;
		var v = cb_obj.value

		var hp = data['hp']
		var accel = data['accel']
		var weight = data['weight']
		var mpg = data['mpg']

		var label = data['label']
		var color = data['color']

		%s[0] = v

		var score =  v * %s + %s * %s + %s * %s + %s * %s

		label[0] = score.toFixed(1)

		
		if (score < 3) {
			color[0]  = '%s'
		}
		else if (score < 4) {
			color[0]  = '%s'
		}
		else {
			color[0]  = '%s'
		}
		

		source.change.emit();
    """

jscode_master2 = """
        var data = source.data;
		var v = cb_obj.value

		var hp = data['hp']
		var accel = data['accel']
		var weight = data['weight']
		var mpg = data['mpg']

		var label = data['label']
		var color = data['color']

		{slider_value}[0] = v //this is the value that is updated by this slider

		var hp_points = 0
		var accel_points = 0
		var weight_points = 0
		var mpg_points = 0
		
		if (hp > {hp_thresh_3}) {{
			hp_points = 5
		}}
		else if (hp > {hp_thresh_2}) {{
			hp_points = 4
		}}
		else if (hp > {hp_thresh_1}) {{
			hp_points = 3
		}}
		else if (hp > {hp_thresh_0}) {{
			hp_points = 2
		}}
		else {{
			hp_points = 1
		}}

		if (accel < {accel_thresh_3}) {{
			accel_points = 5
		}}
		else if (accel < {accel_thresh_2}) {{
			accel_points = 4
		}}
		else if (accel < {accel_thresh_1}) {{
			accel_points = 3
		}}
		else if (accel < {accel_thresh_0}) {{
			accel_points = 2
		}}
		else {{
			accel_points = 1
		}}

		if (weight < {weight_thresh_3}) {{
			weight_points = 5
		}}
		else if (weight < {weight_thresh_2}) {{
			weight_points = 4
		}}
		else if (weight < {weight_thresh_1}) {{
			weight_points = 3
		}}
		else if (weight < {weight_thresh_0}) {{
			weight_points = 2
		}}
		else {{
			weight_points = 1
		}}

		if (mpg < {mpg_thresh_3}) {{
			mpg_points = 5
		}}
		else if (mpg < {mpg_thresh_2}) {{
			mpg_points = 4
		}}
		else if (mpg < {mpg_thresh_1}) {{
			mpg_points = 3
		}}
		else if (mpg < {mpg_thresh_0}) {{
			mpg_points = 2
		}}
		else {{
			mpg_points = 1
		}}

		var score = hp_points * {hp_weight} + accel_points * {accel_weight} + weight_points * {weight_weight} + mpg_points * {mpg_weight}

		label[0] = score.toFixed(1) 

		if (score < 3) {{
			color[0]  = '{red}'
		}}
		else if (score < 4) {{
			color[0]  = '{yellow}'
		}}
		else {{
			color[0]  = '{green}'
		}}

		source.change.emit();
    """