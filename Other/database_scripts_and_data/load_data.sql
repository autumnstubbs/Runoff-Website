-- set global local_infile = true;

-- LOAD DATA LOCAL INFILE 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/location.csv' INTO TABLE location FIELDS TERMINATED by ',' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/daily_info.csv' 
INTO TABLE daily_info 
FIELDS TERMINATED by ',' 
LINES TERMINATED BY '\n'
-- (daily_info_id, location_id, @info_date, precipitation, snowfall, snowmelt, risk)
-- SET info_date = STR_TO_DATE(@info_date,'%Y-%m-%d');

-- select STR_TO_DATE('09-3-01','%Y-%m-%d')
-- select count(*) from daily_info;
-- select * from daily_info where location_id = 3200000;