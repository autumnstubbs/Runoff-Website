from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pyproj
import csv
from itertools import islice
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm

# location of the data (netcdf files)
my_directory = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob'
# location of project (where to store output)
project_dir = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io'

# get x and y points from netcdf file
my_nc_file = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc'
dataset = Dataset(my_nc_file, mode='r+')
variable = dataset.variables["risk_all_10days"][:]
data = variable[0, :, :]
geoy = dataset.variables["y"][:]
geox = dataset.variables["x"][:]

# projection of the current x/y coordinates
projIn = pyproj.Proj(
    '+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')

# desired projection of the output
projOut = pyproj.Proj('epsg:4326')

count = 0
count_y = 0
count_x = 0
WGS84_vals = []
WGS84_points = np.zeros([2001 * 1601, 2], dtype=float)

print("Getting Points")
my_count = 0
for y in data:
    for x in y:
        my_count = my_count + 1
        print(my_count)

        new_x, new_y = pyproj.transform(projIn, projOut, geox[count_x], geoy[count_y])
        WGS84_vals.append(data[count_y][count_x])
        WGS84_points[count] = [new_x, new_y]

        count += 1
        count_x += 1
    count_y += 1
    count_x = 0

file_points = open("WGS84_points_saved", "wb")
file_vals = open("WGS84_vals_saved", "wb")
np.save(file_points, WGS84_points)
np.save(file_vals, WGS84_vals)
file_points.close
file_vals.close
dataset.close()
