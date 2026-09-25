CREATE DATABASE IF NOT EXISTS train_enquiry;

USE train_enquiry;

CREATE TABLE IF NOT EXISTS train_schedule (

    SN INT,

    Train_No INT,

    Station_Code VARCHAR(20),

    `1A` INT,

    `2A` INT,

    `3A` INT,

    SL INT,

    Station_Name VARCHAR(100),

    Route_Number INT,

    Arrival_time TIME,

    Departure_Time TIME,

    Distance DECIMAL(10,2)

);