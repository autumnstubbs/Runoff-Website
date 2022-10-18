import pyproj
import MySQLdb
import random
import geopy
import sys
import json
import ast
from pyproj import Transformer
import math

"""
# gcs_proj = pyproj.Proj('epsg:3857')
gcs_proj = pyproj.Proj('epsg:4326')
pcs_proj = pyproj.Proj('+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')
x, y = pyproj.transform(gcs_proj, pcs_proj, 31.9, -97.8)
"""

"""
transformer = Transformer.from_crs(gcs_proj, pcs_proj)
x, y = transformer.transform(51.9, -97.8)
"""

# p = pyproj.Proj(proj='utm',zone=10,ellps='WGS84', preserve_units=False)
# x,y = p(-120.108, 34.36116666)


"""
gcs = 'epsg:3857'
pcs = '+proj=lcc +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs'
transformer = Transformer.from_crs(gcs, pcs)
x, y = transformer.transform(60, -96)
"""
# print(LatLon_To_XY(51.9, -97.8))



db = MySQLdb.connect("localhost", "root", "pass", "EOF_Website")
my_cursor = db.cursor()


def convert(lat, lon):
    # takes in lat and lon and returns x and y
    gcs_proj = pyproj.Proj('epsg:4326')
    # gcs_proj = pyproj.Proj('epsg:3857')
    pcs_proj = pyproj.Proj(
        '+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')
    return pyproj.transform(gcs_proj, pcs_proj, lat, lon)

def pcs_to_gcs(x, y):
    gcs_proj = pyproj.Proj('epsg:4326')
    pcs_proj = pyproj.Proj(
        '+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')
    return pyproj.transform(pcs_proj, gcs_proj, y, x)


def get_dates():
    # gets a list of dates from database
    # returns them as an array
    query = "SELECT date from eof_website.daily_info where location_id = 1;"
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    return data


def get_date(day_num):
    # takes in a day_num 0 - 9
    # and returns a date in sql format
    return get_dates()[day_num][0]


def get_boundaries(x, y):
    # takes in x and y values (floats)
    # returns an array with the boundaries of each x, y location
    # in the following form: [a, b, c, d] (where a, b, c, d are floats)
    # where a is 500 meters left of x, b is 500 meters right of x
    # and c is 500 meters below y, and d is 500 meters above y
    return [x - 1000, x + 1000, y - 1000, y + 1000]


def get_data(lat, lon, day_num):
    x, y = convert(lat, lon)
    date = get_date(day_num)
    boundaries = get_boundaries(x, y)
    query1 = "select location_id from eof_website.location where LOWER_X_BOUND >= " + str(boundaries[0]) + " and upper_x_BOUND <= " + str(boundaries[1]) + " and lower_y_bound >= " + str(boundaries[2]) + " and  UPPER_Y_BOUND <= " + str(boundaries[3]) + ";"
    my_cursor.execute(query1)
    data = my_cursor.fetchall()[0]
    query2 = "select * from eof_website.daily_info where location_id = " + str(data[0]) + " and date = DATE('" + str(date) + "');"
    my_cursor.execute(query2)
    data = my_cursor.fetchall()
    return data


def format_data(lat, lon, day_num):
    # takes in lat, lon, day_num and
    # returns data in a format that is ready to be sent to javascript
    # in the form [risk, rainfall, snowmelt, snowfall]
    data = get_data(lat, lon, day_num)[0]
    risk = ['NONE', 'MINIMAL', 'MODERATE', 'HIGH']
    water_data = [data[3], data[4], data[5]]
    for count in range(3):
        if water_data[count] is None:
            water_data[count] = 0
    info = [risk[random.randint(0, 3)], water_data[0], water_data[1], water_data[2]]
    if info[0] == None:
        info[0] = 'NONE'
    return info


def main():
    # lat = sys.argv[1]
    # lon = sys.argv[2]

    # data = format_data(41.210687178410154, -77.904567592435, 0)
    lat = 48.7132
    lon = -68.9932
    x, y = convert(lat, lon)
    new_lat, new_lon = pcs_to_gcs(x, y)
    print("Original Longitude: " + str(lon))
    print("New Longitude: " + str(new_lon))
    print("Original Latitude: " + str(lat))
    print("New Latitude: " + str(new_lat))
    print("X:")
    print(x)
    print("Y:")
    print(y)

    """
    for day in range(10):
        print(format_data(41.36639065935512, -75.65262179828818, day))
    """

    # print(get_data(41.210687178410154, -77.904567592435, 0))
    # print(format_data(41.210687178410154, -77.904567592435, 0))

    # print(json.dumps(data))
    # sys.stdout.flush()

    # convert address to lat/lon
    # return info for that day


if __name__ == "__main__":
    main()

