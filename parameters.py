colors = {'white': '#ffffff', 'gray': '#888888', 'red': '#de4307', 'yellow': '#f6d04d', 'green': '#8bc24c'}

weights = {'hp': 0.2, 'accel': 0.3, 'weight': 0.1, 'mpg': 0.4}

thresholds = {'acceleration': {14.7:2, 13.8:3, 13:4, 11.3:5},
        'liters_per_100km': {9.4:2, 8.1:3, 7.3:4, 6.4:5},
        'weight_kg': {1170: 2, 1010: 3, 950: 4, 870: 5}, 
        'horsepower': {100: 2, 125: 3, 150: 4, 180: 5}} #the higher the better, reverse = True

quality_weight, price_weight = 0.7, 0.3	