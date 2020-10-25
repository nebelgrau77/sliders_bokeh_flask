points = {'accel': {14.7:2, 13.8:3, 13:4, 11.3:5}, # the lower the better
        'mpg': {9.4:2, 8.1:3, 7.3:4, 6.4:5}, # the lower the better  }
        'weight': {1170: 2, 1010: 3, 950: 4, 870: 5}, # the lower the better
        'horsepower': {100: 2, 125: 3, 150: 4, 180: 5} # the HIGHER the better, reverse = True
        }

def dataframe(dbfile, tablename):
    conn = sqlite.connect(dbfile)
    df = pd.read_sql_query('''SELECT * FROM {}'''.format(tablename), conn)
    return df


def assign_points(df, col, points, reverse = False):    
    points_col = '{}_points'.format(col) 
    
    if reverse == True:    
        for w in points.keys():    
            df.loc[df[col] > w, points_col] = points[w]
    else: 
        for w in points.keys():    
            df.loc[df[col] < w, points_col] = points[w]
            
    df.loc[df[points_col].isna(), points_col] = 1
    return df

def assign_cyl_points(df):
    for c, p in zip([6,8,4], [5,4,3]):
        df.loc[df['cylinders'] == c, 'cylinders_points'] = p
    return df