from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pyproj
import csv
from itertools import islice
import matplotlib.colors as mcolors
import cv2
from matplotlib.colors import LogNorm
import cv2

# location of the data (netcdf files)
my_directory = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob'
# location of project (where to store output)
project_dir = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io'

colors = [
    '#778899', # gray
    '#fdae61',
    '#66c2a5',

    '#93c47d', # green
    '#abdda4',
    '#93c47d', # also green

    '#f79862', # orange

    '#d53e4f',
    '#f46d43',
    '#9e0142'] # red

cmap_name = 'my_list'
cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=4)

# read files
file_points = open("python_scripts/WGS84_points_saved", "rb")
file_vals = open("python_scripts/WGS84_vals_saved", "rb")
WGS84_points = np.load(file_points)
WGS84_vals = np.load(file_vals)
file_points.close()
file_vals.close()

points = WGS84_points[0:3203601]
values = WGS84_vals[0:3203601]

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
    plt.savefig(project_dir + '/temp_img/Event' + str(i) + '_projected.png', transparent=True)
    # plt.savefig(project_dir + '/temp_img/Event' + str(i) + '_projected.png', transparent=True)
    plt.close()
    # src = cv2.imread(project_dir + '/temp_img/Event' + str(i) + '_projected.png')
    # img = cv2.rotate(src, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    # img = cv2.flip(img, 1)
    # cv2.imwrite(project_dir + '/temp_img/Event' + str(i) + '_projected.png', img)