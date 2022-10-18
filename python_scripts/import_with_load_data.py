import netCDF4 as nc
# USE XARRAY INSTEAD!!!
import numpy as np
from numpy import ma
import sys
# import mysql.connector
import MySQLdb

"""
NOTE:
Before running this, go to mysql command line and run the following command:
$ show global variables like 'local_infile';
if local_infile is off, run:
$ set global local_infile = true;
"""

# connecting to the database
db = MySQLdb.connect("localhost", "root", "pass", "final_database")

# creating cursor to manipulate database
my_cursor = db.cursor()
"""
query = "LOAD DATA LOCAL INFILE 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project" \
        ".github.io/location.csv' INTO TABLE test_2 FIELDS TERMINATED by ',' LINES TERMINATED BY '\n' "
"""
query = "select * from daily_info where daily_info_id = 1"
# query = "select count(*) from daily_info"
my_cursor.execute(query)
data = my_cursor.fetchall()
print(data)
