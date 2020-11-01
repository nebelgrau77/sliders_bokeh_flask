import sqlite3 as sqlite
import pandas as pd
from parameters import thresholds

'''
points = {'acceleration': {14.7:2, 13.8:3, 13:4, 11.3:5},
        'liters_per_100km': {9.4:2, 8.1:3, 7.3:4, 6.4:5},
        'weight_kg': {1170: 2, 1010: 3, 950: 4, 870: 5}, 
        'horsepower': {100: 2, 125: 3, 150: 4, 180: 5}} #the higher the better, reverse = True
'''

def dataframe(dbfile, tablename):
    conn = sqlite.connect(dbfile)
    df = pd.read_sql_query('''SELECT * FROM {}'''.format(tablename), conn)
    return df


def assign_points(df, col, thresholds, reverse = False):    
    points_col = '{}_points'.format(col) 
    
    if reverse == True:    
        for w in thresholds.keys():    
            df.loc[df[col] > w, points_col] = thresholds[w]
    else: 
        for w in thresholds.keys():    
            df.loc[df[col] < w, points_col] = thresholds[w]
            
    df.loc[df[points_col].isna(), points_col] = 1
    return df

def assign_cyl_points(df):
    for c, p in zip([6,8,4], [5,4,3]):
        df.loc[df['cylinders'] == c, 'cylinders_points'] = p
    return df

	
def dataframe_points(dbfile, tablename, points):	
	data = dataframe(dbfile, tablename)
	data = assign_points(data, 'horsepower', thresholds['horsepower'], reverse=True)
	data = assign_points(data, 'acceleration', thresholds['acceleration'])
	data = assign_points(data, 'weight_kg', thresholds['weight_kg'])
	data = assign_points(data, 'liters_per_100km', thresholds['liters_per_100km'])
	data = assign_cyl_points(data)
	return data


'''

COULD BE AN IDEA


In [1]: acceleration =  {14.7:2, 13.8:3, 13:4, 11.3:5}

In [2]: acceleration.keys()
Out[2]: dict_keys([14.7, 13.8, 13, 11.3])

In [3]: a = 12

In [4]: for x in acceleration.keys():
   ...:     if a > x:
   ...:         print(x)
   ...: 
11.3

In [5]: for x in acceleration.keys():
   ...:     if a < x:
   ...:         print(x)
   ...: 
   ...: 
14.7
13.8
13

In [6]: for x in acceleration.keys():
   ...:     if a < x:
   ...:         t = x
   ...: print(acceleration[t])
   ...: 
   ...: 
   ...: 
4


IT WON'T WORK FOR VALUES BELOW THE FIRST THRESHOLD

'''