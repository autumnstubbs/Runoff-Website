from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pyproj
import csv
from itertools import islice
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm


""" Switch these to use gdrive or Silber's drive """
# my_directory = 'D:/whole_prob/'
# my_directory = 'G:\My Drive\CISC498_project_copy\whole_prob'
my_directory = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob'
project_dir = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io'
"""

PART 1: Reprojection

Reprojects points using a python library I found.

Takes very long time! I ran once, stored them in temp files,
then commented out so I could experiment with the drawing.

Temp files read from in part 2.

"""

# COMMENTING THIS OUT TO REDRAW IMAGES
"""

# my_nc_file = my_directory + '/pF.nc'
# my_nc_file = my_directory + '/p1.nc'
my_nc_file = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc'
dataset = Dataset(my_nc_file, mode='r+')
# variable = dataset.variables["EVENT"][:]
variable = dataset.variables["risk_all_10days"][:]
data = variable[0, :, :]
geoy = dataset.variables["y"][:]
geox = dataset.variables["x"][:]

# web mercator
# projOut = pyproj.Proj('epsg:3395')
projOut = pyproj.Proj('epsg:4326')
# projOut = pyproj.Proj('epsg:3857')

# my best approximation of what the current projection is
projIn = pyproj.Proj(
    '+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')

count = 0
count_y = 0
count_x = 0
mercator_vals = []
mercator_points = np.zeros([2001 * 1601, 2], dtype=float)

def gcs_to_pcs(lat, lon):
    # takes in lat and lon and returns x and y
    gcs_proj = pyproj.Proj('epsg:4326')
    pcs_proj = pyproj.Proj('epsg:3857')
    return pyproj.transform(gcs_proj, pcs_proj, lat, lon)

def pcs_to_gcs(x, y):
    gcs_proj = pyproj.Proj('epsg:4326')
    pcs_proj = pyproj.Proj(
        '+proj=lcc +a=6370000.0 +b=6370000.0 +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +k=1 +units=m +nodefs')
    return pyproj.transform(pcs_proj, gcs_proj, y, x)

print("Getting Points")
my_count = 0
for y in data:
    for x in y:
        my_count = my_count + 1
        print (my_count)

        # new_lat, new_lon = pcs_to_gcs(geox[count_x], geoy[count_y])
        # new_x, new_y = gcs_to_pcs(new_lat, new_lon)
        
        new_x, new_y = pyproj.transform(projIn, projOut, geox[count_x], geoy[count_y])
        new_x, new_y = pyproj.transform(projIn, projOut, geox[count_x], geoy[count_y])
        mercator_vals.append(data[count_y][count_x])
        mercator_points[count] = [new_x, new_y]

        # print("point: ", mercator_points[count], "val: ", data[count_x][count_y])
        count += 1
        count_x += 1
    count_y += 1
    count_x = 0

file_points = open("mercator_points_saved", "wb")
file_vals = open("mercator_vals_saved", "wb")
np.save(file_points, mercator_points)
np.save(file_vals, mercator_vals)
file_points.close
file_vals.close
dataset.close()
"""
# END OF COMMENT

# ********************************************************************************
# ********************************************************************************

"""

PART 2: Draw reprojected image

First builds same colormap Prof Hu used.

2 options:
Risk images: Create risk view (one that people actually see)
Var images: Create image that website can pull rgb data from to determine rain, snowfall, etc.

"""

""" Build colormap """

colors = [
    '#3288bd', # used - blue
    '#fdae61',
    '#66c2a5',

    '#e6f598', # used - yellow?
    '#abdda4',
    '#fee08b',# used - yellow?

    '#5e4fa2', # used -purple

    '#d53e4f',
    '#f46d43',
    '#9e0142'] # used - red

colors_1 = [
    '#93c47d', # used - 1 - now green
    '#fdae61',
    '#66c2a5',

    '#e6f598', # used - 2? still yellow
    '#abdda4',
    '#fee08b',# used - 2?

    '#f79862', # used - 3 now orange

    '#d53e4f',
    '#f46d43',
    '#9e0142'] # used - 4 still red

colors_2 = [
    '#778899', # used - 1 - now gray
    '#fdae61',
    '#66c2a5',

    '#93c47d', # used - 2? now green
    '#abdda4',
    '#93c47d',# used - 2? now green

    '#f79862', # used - 3 now orange

    '#d53e4f',
    '#f46d43',
    '#9e0142'] # used - 4 still red

# n_bin = [3, 6, 10, 100]  # Discretizes the interpolation into bins

cmap_name = 'my_list'
cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors_2, N=4)

""" Read from temp files """

file_points = open("mercator_points_saved", "rb")
file_vals = open("mercator_vals_saved", "rb")
mercator_points = np.load(file_points)
mercator_vals = np.load(file_vals)
file_points.close()
file_vals.close()

points = mercator_points[0:3203601]
values = mercator_vals[0:3203601]

min_x = min(points[:, 0])
max_x = max(points[:, 0])
min_y = min(points[:, 1])
max_y = max(points[:, 1])

""" flip image vertically, idk why its upside down normally """

points_new = np.zeros([2001 * 1601, 2], dtype=float)

for i in range(len(points)):
    col_num = i // 2001
    row_num = i % 2001
    reverse_col_num = 1600 - col_num
    points_new[i] = points[2001 * reverse_col_num + row_num]

grid_x, grid_y = np.mgrid[min_x:max_x:2001j, min_y:max_y:1601j]

""" CREATE RISK IMAGES """

# my_nc_file = my_directory + '/pF.nc'
# my_nc_file = my_directory + '/p1.nc'
# my_nc_file = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/p1.nc'
my_nc_file = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc'
dataset = Dataset(my_nc_file, mode='r+')
# variable = dataset.variables["EVENT"][:]
variable = dataset.variables["risk_all_10days"][:]

print("Plotting")

for i in range(10):
    print("Day: " + str(i))
    count_x = 0
    count_y = 0
    new_vals = []
    data = variable[i, :, :]
    # data = (data - 0.0 / (200.0 - 0.0)) #scale data from 0.0 to 1.0 (where max is 200, min is 0)
    for y in data:
        print("Day: " + str(i))
        print("y: " + str(y))
        count_x = 0
        for x in y:
            new_vals.append(data[count_y][count_x])
            count_x += 1
        count_y += 1
    grid = griddata(points_new, new_vals, (grid_x, grid_y), method="linear")
    fig = plt.figure(figsize=(16, 16))
    plt.imshow(grid.T, extent=(min_x, max_x, min_y, max_y), origin='lower', cmap=cmap)
    plt.axis('off')
    plt.savefig(project_dir + '/new_images_4326/new_colors/Event' + str(i) + '_projected.png', transparent=True)
    plt.close()

""" CREATE VAR IMAGES """
"""
var_file = my_directory + '/vF.nc'

dataset = Dataset(var_file, mode='r+')
var1 = dataset.variables["ACCPRCP"][:]
var2 = dataset.variables["ACSNOM"][:]
var3 = dataset.variables["QSNOW"][:]
dataset.close()

for j in range(10):    
    count_x = 0
    count_y = 0
    vals_accprcp = []
    vals_acsnom = []
    vals_qsnow = []
    data_accprcp = var1[j, :, :]
    data_acsnom = var2[j, :, :]
    data_qsnow = var3[j, :, :]

    for y in data:
        count_x = 0
        for x in y:
            vals_accprcp.append(data_accprcp[count_y][count_x])
            vals_acsnom.append(data_acsnom[count_y][count_x])
            vals_qsnow.append(data_qsnow[count_y][count_x])
            count_x+=1
        count_y+=1


    grid_accprcp = griddata(points_new, vals_accprcp, (grid_x, grid_y), method='linear')
    grid_acsnom = griddata(points_new, vals_acsnom, (grid_x, grid_y), method='linear')
    grid_qsnow = griddata(points_new, vals_qsnow, (grid_x, grid_y), method='linear')

    ind = 0
    ind_x = 0
    ind_y = 0
    rgba = np.zeros((1601, 2001, 4), dtype=float)
    for y in grid_accprcp:
        ind_x = 0
        for x in y:
            if (not np.isnan(x)):
                rgba[ind_x][ind_y] = [grid_accprcp[ind_y][ind_x] / 200.0, grid_acsnom[ind_y][ind_x] / 200.0, grid_qsnow[ind_y][ind_x] / 200.0, 1.0]
            ind_x+=1
        ind_y+=1

    fig = plt.figure(figsize=(16, 16))
    plt.imshow(rgba, extent=(min_x, max_x, min_y, max_y), origin='lower')
    plt.axis('off')
    plt.savefig(my_directory + '/images/Event' + str(j) + '_vars.png', transparent=True)
    plt.close()
"""
