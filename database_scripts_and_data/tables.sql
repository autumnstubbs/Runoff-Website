CREATE TABLE `location` (
`LOCATION_ID` int NOT NULL,
`X` float NOT NULL,
`Y` float NOT NULL,
PRIMARY KEY (`LOCATION_ID`),
UNIQUE KEY `ID_UNIQUE` (`LOCATION_ID`)) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `daily_info` (
`DAILY_INFO_ID` int NOT NULL,
`LOCATION_ID` int NOT NULL,
`INFO_DATE` int NOT NULL,
`PRECIPITATION` float DEFAULT NULL,
`SNOWFALL` float DEFAULT NULL,
`SNOWMELT` float DEFAULT NULL,
`RISK` int DEFAULT NULL,
PRIMARY KEY (`DAILY_INFO_ID`),
KEY `daily_info_fk1` (`LOCATION_ID`),
CONSTRAINT `daily_info_fk1` FOREIGN KEY (`LOCATION_ID`) REFERENCES `location` (`LOCATION_ID`)) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci