# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:09:01 2021

@author: widmer
"""


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
    



