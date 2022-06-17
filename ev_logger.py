# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:09:01 2021

@author: widmer
"""
from statistics import mean

def get_operator_status(date, data):
    occupied = 0
    available = 0
    outofservice = 0
    unknown = 0
    length = len(data)
    for i in range(length):
        if data[i]["EVSEStatus"] == 'Occupied':
            occupied = occupied+1
        if data[i]["EVSEStatus"] == 'Available':
            available = available+1    
        if data[i]["EVSEStatus"] == 'OutOfService' :
            outofservice = outofservice+1 
        if data[i]["EVSEStatus"] == 'Unknown' :
            unknown = unknown+1 
    return [date, occupied, available, unknown, outofservice]

def get_station_status(data, station):
    length = len(data)
    for i in range(length):
        if data[i]["EvseID"] == station:
            return data[i]['EVSEStatus']

def print_network(name, list):
    print(name , "            ", list)
    
def log_csv(filename, data, fields):
    import csv
    import os
     
        
    # data rows of csv file  
    is_empty =  os.path.exists(filename) == 0
    with open(filename, 'a') as f: 
          
        # using csv.writer method from CSV package 
        write = csv.writer(f, delimiter=',',lineterminator='\r') 
        if is_empty: write.writerow(fields) 
        write.writerow(data) 
        f.close()

def calculate_useage_per_day(date, useage):
    date_counter = 0
    useage_daily = []
    date_day = []
    for i in range(len(date)-1):
        date_counter = date_counter +1
        #compare strings if new date found make new entry
        if(date[i][0:10] != date[i+1][0:10]):
            #new day entry found
            date_day.append(date[i][0:10])
            #todo calculate average
            useage_daily.append(mean(useage[i-date_counter+1:i]))
            date_counter = 0 
    return [date_day, useage_daily]

def calculate_session_per_day(date, sessions):
    date_counter = 0
    session_daily = []
    date_day = []
    for i in range(len(date)-1):
        date_counter = date_counter +1
        #compare strings if new date found make new entry
        if(date[i][0:10] != date[i+1][0:10]):
            #new day entry found
            date_day.append(date[i][0:10])
            session_daily.append((sessions[i]-sessions[i-date_counter]))
            date_counter = 0 
    #fix first error calculation
    session_daily[0] = 0
    return [date_day, session_daily]    



