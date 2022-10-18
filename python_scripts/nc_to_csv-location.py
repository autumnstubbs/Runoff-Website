import numpy as np
from numpy import ma
import netCDF4 as nc
import csv

#filepath for csv to write to
filepath = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/location.csv"
# file for x/y values
risk_file = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc"
# get dataset from file
risk_dataset = nc.Dataset(risk_file)
# get necessary arrays
x = risk_dataset["x"][:]
y = risk_dataset["y"][:]
# get data for x/y
file_points = open("C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/mercator_points_saved", "rb")
mercator_points = np.load(file_points)
file_points.close()

points = mercator_points[0:3203601]
print(points.shape)
print(points[3203600])

# loops to get risk data
location_arr = []
location_id = 0
# loop across y
for i in range(2001):
    # loop across x
    for j in range(1601):
        location_id = location_id + 1
        print("X: " + str(i) + " Y: " + str(j))
        # loop across dates
        local_x = x[i]
        local_y = y[j]
        local_data = [location_id, local_x, local_y]
        location_arr.append(local_data)

with open(filepath, 'w', newline='') as file:
    wr = csv.writer(file, delimiter=',')
    wr.writerows(location_arr)
# close file
file.close()
