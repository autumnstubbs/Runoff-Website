import netCDF4 as nc
# USE XARRAY INSTEAD!!!
import numpy as np
from numpy import ma
import sys
# import mysql.connector
import MySQLdb

# connecting to the database
db = MySQLdb.connect("localhost", "root", "pass", "EOF_Website")

"""
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pass",
    database="EOF_Website" # comment this line if you do not have a database yet, then read below
)
"""

# if the database does not already exist, you can create it by uncommenting the following line
# my_cursor.execute("CREATE DATABASE EOF_Website")
# after you run this, uncomment the database field in the connect function above

# creating cursor to manipulate database
my_cursor = db.cursor()





"""
file_name = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc"
dataset = nc.Dataset(file_name)
"""
# to get data info
# runoff = dataset["risk_all_10days"]
# to get data
"""
runoff = dataset["risk_all_10days"][:]
precipitation = dataset["ACCPRCP_Med"][:]
snowfall = dataset["QSNOW_Med"][:]
snowmelt = dataset["ACSNOM_Med"][:]
"""
# to get dimensions
"""
runoff.shape
"""
# to get a row of data
"""
runoff[0, 0, 0]
"""


def get_boundaries(x, y):
    # takes in x and y values (floats)
    # returns an array with the boundaries of each x, y location
    # in the following form: [a, b, c, d] (where a, b, c, d are floats)
    # where a is 500 meters left of x, b is 500 meters right of x
    # and c is 500 meters below y, and d is 500 meters above y
    return [x - 500, x + 500, y - 500, y + 500]


def get_location_info(x_array, y_array, x_index, y_index):
    # take in x and y arrays of floats and desired x, y indices
    # returns the location boundaries at that location
    x = x_array[x_index]
    y = y_array[y_index]
    return get_boundaries(x, y)


def get_water_info(precipitation_array, snowfall_array, snowmelt_array, x_index, y_index, day):
    # takes in indexes of floats for precipitation, snowfall, and snowmelt
    # as well as x, y indices and a day (0 - 9)
    # returns an array of floats with information for that day and location:
    # [precipitation, snowfall, snowmelt]
    precipitation_value = precipitation_array[day, y_index, x_index]
    snowfall_value = snowfall_array[day, y_index, x_index]
    snowmelt_value = snowmelt_array[day, y_index, x_index]
    return [precipitation_value, snowfall_value, snowmelt_value]


def insert_location_info(location_id, info):
    # takes in an id integer and an array from get_location_info
    # inserts a row into location_info
    query = "insert into location values (" + str(location_id) + "," + str(info[0]) + "," + str(info[1]) + "," + str(info[2]) + "," + str(info[3]) + ");"
    my_cursor.execute(query)
    db.commit()


def insert_daily_info(daily_info_id, location_id, info, date):
    # takes in an id integer, an array from get_water_info, and a date
    # as well as x, y indices and a day (0 - 9)
    # inserts a row into the daily_info table

    query1 = "insert into daily_info (daily_info_id, location_id, date) values ("
    query2 = "insert into daily_info values ("
    query = ""

    if info[0] is ma.masked:
        # if there is no data, insert only the id and date
        query = query1 + str(daily_info_id) + "," + str(location_id) + "," + "'" + str(date) + "'" + ");"
    else:
        # insert all data
        query = query2 + str(daily_info_id) + "," + str(location_id) + "," + "'" + str(date) + "'" + "," + str(info[0]) + "," + str(info[1]) + "," + str(info[2]) + ");"

    my_cursor.execute(query)
    db.commit()
    return 0


def get_risk_info(x, y, day, risk_arr):
    # takes in an values for x, y, and date, and risk array
    # and returns the risk value for that day and location
    return risk_arr[day, y, x]


def insert_risk_info(x, y, day, date, location_id, risk_arr):
    # takes in values for x, y, day, date, location_id, and an array of risk values
    # and generates a string to insert that specific data into a mysql database
    risk = get_risk_info(x, y, day, risk_arr)
    if risk is ma.masked:
        risk = 0
    query = "update eof_website.daily_info set RISK=" + str(risk) + " where LOCATION_ID=" + str(location_id) + " and DATE=" + "'" + str(date) + "'" + ";"
    my_cursor.execute(query)
    db.commit()


def main():
    # get files
    # risk_file_contains daily info about risk, and overview info for precipitation and snow
    risk_file = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc"
    # water file contains daily information for precipitation and snow
    water_file = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/vF.nc"

    # define datasets
    risk_dataset = nc.Dataset(risk_file)
    water_dataset = nc.Dataset(water_file)

    # get necessary arrays
    x = risk_dataset["x"][:]
    y = risk_dataset["y"][:]
    precipitation = water_dataset["ACCPRCP"][:]
    snowfall = water_dataset["QSNOW"][:]
    snowmelt = water_dataset["ACSNOM"][:]
    risk = risk_dataset["risk_all_10days"][:]

    query = "LOAD DATA LOCAL INFILE 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project" \
            ".github.io/location.csv' INTO TABLE import_test FIELDS TERMINATED by ',' LINES TERMINATED BY '\n' "
    my_cursor.execute(query)

    """
    date = '2009-12-20'
    dates = [date]
    for count in range(9):
        query = "SELECT DATE_ADD('" + date + "', INTERVAL 1 day);"
        my_cursor.execute(query)
        date_array = my_cursor.fetchall()
        date = str(date_array[0][0])
        dates.append(date)
        # dates.append(start_date[0][0])

    # import risk here
    location_id = 590103
    # loop across y
    for i in range(372, x.shape[0] - 1):
        # loop across x
        for j in range(1106, y.shape[0] - 1):
            day = 0
            location_id = location_id + 1
            print(location_id)
            print("X: " + str(i) + " Y: " + str(j))
            # loop across dates
            for date in dates:
                insert_risk_info(i, j, day, date, location_id, risk)
                day = day + 1
    """

    """
    location_id = 0
    daily_info_id = 0
    # loop across y
    for i in range(x.shape[0] - 1):
            # loop across x
            for j in range(y.shape[0] - 1):
                print(location_id)
                day = 0
                location_id = location_id + 1
                insert_location_info(location_id, get_location_info(x, y, i, j))
                # loop across dates
                for date in dates:
                    daily_info_id = daily_info_id + 1
                    insert_daily_info(daily_info_id, location_id, get_water_info(precipitation, snowfall, snowmelt, i, j, day), date)
                    day = day + 1
    """

    """
    my_cursor.execute('select * from eof_website.location where location_id = 3200000')
    data = my_cursor.fetchall()
    print(data)
    print(data[0][0])
    """

    """
    currx = 1500
    curry = 1500
    print('X: ' + str(x[currx]))
    print('Y: ' + str(y[curry]))
    print('Boundaries: ' + str(get_boundaries(x[currx], y[curry])))
    print('\n' + "FROM FILE")
    print("Precipitation:")
    for x in range(9):
        print(str(precipitation[x, curry, currx]))
    print("Snowfall:")
    for x in range(9):
        print(str(snowfall[x, curry, currx]))
    print("Snowmelt:")
    for x in range(9):
        print(str(snowmelt[x, curry, currx]))

    print("FROM DATABASE")
    """


    # insert location info
    # insert daily info

    # location_info = get_location_info(x, y, 0, 0)
    # water_info = get_water_info(precipitation, snowfall, snowmelt, 0, 0, 0)
    # insert_location_info(1, location_info)
    # insert_daily_info(1, water_info, '2022-07-17')


    """
    location_id = 0
    location_info = get_location_info(x, y, 1500, 1500)
    insert_location_info(location_id, location_info)
    for count in range(10):
        water_info = get_water_info(precipitation, snowfall, snowmelt, 1500, 1500, count)
        insert_daily_info(count, location_id, water_info, dates[count])
    """

    """
    for count in range(10):
        print("DAY " + str(count))
        print("Precipitation: " + str(precipitation[count, 1500, 1500]))
        print("Snowfall: " + str(snowfall[count, 1500, 1500]))
        print("Snowmelt: " + str(snowmelt[count, 1500, 1500]))
        water_info = get_water_info(precipitation,snowfall, snowmelt, 1500, 1500, count)
        print("daily_info: " + str(water_info))
    """

if __name__ == "__main__":
    main()
