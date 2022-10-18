import numpy as np
from numpy import ma
import netCDF4 as nc
import csv

# files where data is stored
risk_file = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/days10.nc"
water_file = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/whole_prob/vF.nc"
# create nc datasets
risk_dataset = nc.Dataset(risk_file)
water_dataset = nc.Dataset(water_file)
# data arrays
risk = risk_dataset["risk_all_10days"][:]
precipitation = water_dataset["ACCPRCP"][:]
snowfall = water_dataset["QSNOW"][:]
snowmelt = water_dataset["ACSNOM"][:]

print(risk.shape)
print(risk[:, 0, 0])

# open csv
filepath = "C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/daily_info.csv"

# get date values
# dates = ['2009-12-20', '2009-12-21', '2009-12-22', '2009-12-23', '2009-12-24', '2009-12-25', '2009-12-26', '2009-12-26', '2009-12-28', '2009-12-29']
dates = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# loops to get risk data
daily_info_arr = []
daily_info_id = 0
location_id = 0
# loop across y
for i in range(2001):
    # loop across x
    for j in range(1601):
        location_id = location_id + 1
        print("X: " + str(i) + " Y: " + str(j))
        # loop across dates
        for day in range(0, 10):
            daily_info_id = daily_info_id + 1
            # precipitation[day, y, x]
            daily_precipitation = precipitation[day, j, i]
            # snowfall[day, y, x]
            daily_snowfall = snowfall[day, j, i]
            # snowmelt[day, y, x]
            daily_snowmelt = snowmelt[day, j, i]
            # risk[day, y, x]
            daily_risk = risk[day, j, i]

            if daily_precipitation is ma.masked:
                daily_precipitation = 0
            if daily_snowfall is ma.masked:
                daily_snowfall = 0
            if daily_snowmelt is ma.masked:
                daily_snowmelt = 0
            if daily_risk is ma.masked:
                daily_risk = 0

            daily_info = [daily_info_id, location_id, daily_precipitation, dates[day], daily_snowfall, daily_snowmelt, daily_risk]
            daily_info_arr.append(daily_info)

# print(risk_arr)
# write data
# risk_arr = np.array(risk_arr)
# print(risk_arr)

with open(filepath, 'w', newline='') as file:
    wr = csv.writer(file, delimiter=',')
    wr.writerows(daily_info_arr)
# close file
file.close()
