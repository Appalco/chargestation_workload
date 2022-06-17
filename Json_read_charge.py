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
    
          

url_link = "https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/status/oicp/ch.bfe.ladestellen-elektromobilitaet.json"
url_link_static = "https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json"

import urllib.request, json 
with urllib.request.urlopen(url_link) as url:
    data = json.loads(url.read().decode())
with urllib.request.urlopen(url_link_static) as url:
    data_static = json.loads(url.read().decode())



ev_status = data["EVSEStatuses"]

#extract data for all charging networks
length = len(ev_status)
for i in range(length):
    if ev_status[i]['OperatorName'] == 'Swisscharge':
        swisscharge = ev_status[i]["EVSEStatusRecord"] 
    if ev_status[i]['OperatorName'] == 'evpass':
        evpass = ev_status[i]["EVSEStatusRecord"] 
    if ev_status[i]['OperatorName'] == 'PLUG’N ROLL':
        plug_nroll = ev_status[i]["EVSEStatusRecord"] 
    if ev_status[i]['OperatorName'] == 'Fastned':
        fast_ned = ev_status[i]["EVSEStatusRecord"] 
    if ev_status[i]['OperatorName'] == 'eCarUp':
        ecarup = ev_status[i]["EVSEStatusRecord"] 
    if ev_status[i]['OperatorName'] == 'Move':
        move = ev_status[i]["EVSEStatusRecord"]

from datetime import datetime

now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M")	

swisscharge_list = get_operator_status(date_time, swisscharge)
fast_ned_list = get_operator_status(date_time, fast_ned)
plugn_roll_list = get_operator_status(date_time, plug_nroll)
evpass_list = get_operator_status(date_time, evpass)
move_list = get_operator_status(date_time, move)
ecarup_list = get_operator_status(date_time, ecarup)



# field names  
fields = ['Date', 'Occupied', 'Available', 'Outofservice', 'Unknown']  

print_out = 0
if print_out == 1 :
    print("Date                            Occupied | Available | Outofservice | Unknown")
    print_network("Swisscharge", swisscharge_list )
    print_network("Fast Ned", fast_ned_list )
    print_network("evPass", evpass_list )
    print_network("Plugnroll", plugn_roll_list)
    print_network("EcarUP", ecarup_list )
    print_network("Move", move_list )

log_csv("swisscharge.csv", swisscharge_list, fields)
log_csv("fastned.csv", fast_ned_list, fields )
log_csv("evPass.csv", evpass_list, fields )
log_csv("Plugnroll.csv", plugn_roll_list, fields)
log_csv("EcarUP.csv", ecarup_list, fields )
log_csv("Move.csv", move_list, fields )




