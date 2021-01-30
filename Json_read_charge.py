# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:09:01 2021

@author: widmer
"""

def get_load(data):
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
    return [occupied, available, unknown, outofservice]

def print_network(name, list, date):
    print(dateTimeObj, "   ",name , "            ", list)
    if list[0] != 0:
        print(dateTimeObj, "   ", name , "Workload [%]", (list[1]-list[2])/list[0] )
    else:
        print(dateTimeObj, "   ", name , "Workload [%]",0)
    
    
          

url_link = "https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/status/oicp/ch.bfe.ladestellen-elektromobilitaet.json"

import urllib.request, json 
with urllib.request.urlopen(url_link) as url:
    data = json.loads(url.read().decode())



ev_status = data["EVSEStatuses"]

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
    if ev_status[i]['OperatorName'] == 'easy4you':
        easy4you = ev_status[i]["EVSEStatusRecord"]
    if ev_status[i]['OperatorName'] == 'Move':
        move = ev_status[i]["EVSEStatusRecord"]


swisscharge_list = get_load(swisscharge)
fast_ned_list = get_load(fast_ned)
plugn_roll_list = get_load(plug_nroll)
evpass_list = get_load(evpass)
easy4you_list = get_load(easy4you)
move_list = get_load(move)
ecarup_list = get_load(ecarup)


from datetime import datetime
dateTimeObj = datetime.now()
print("Date                            Occupied | Available | Outofservice | Unknown")
print_network("Swisscharge", swisscharge_list, dateTimeObj )
print_network("Fast Ned", fast_ned_list, dateTimeObj )
print_network("evPass", evpass_list, dateTimeObj )
print_network("Plugnroll", plugn_roll_list, dateTimeObj )
print_network("EcarUP", ecarup_list, dateTimeObj )
print_network("Easy4you", easy4you_list, dateTimeObj )
print_network("Move", move_list, dateTimeObj )