# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:09:01 2021

@author: widmer
"""

import ev_logger as ev_logger
    
          

url_link = "https://teslalogger.de/suc-map2.php"

import json
import urllib.request
x = urllib.request.urlopen(url_link)
raw_data = x.read()
encoding = x.info().get_content_charset('utf8')  # JSON default
php_string = str(raw_data)   #this is data in string format



#Create a string list of all SuCs
start = 0
end = 0
index_start = 0
index_end = 0
suc_list = []
string_offset = 13

##extract all SUCs from PHP source code into a string list
while index_start < len(php_string):
    #◘search for new Supercharger entry
    new_index = php_string.find("var t",index_start)
    index_start = new_index
    if index_start == -1:
        break
    else:
        index_end = php_string.find("';",index_start)
        #search for end of Supercharger entry
        suc_list.append(php_string[index_start+string_offset:index_end])
        print(php_string[index_start+string_offset:index_end])
        index_start = index_end
        
        
#Todo: we need to define here if we want to save all data to csv.
#Also data is probably dynamic so we need to set the data to headers

start = 0
end = 0
index_start = 0
index_end = 0
string_offset = 13
suc_swisslist = []
suc_swisslist_int = []
csv_header = []


#Reduce data to Switzerland only
for i in range(len(suc_list)):
    #◘search for Switzerland keyword
    index = suc_list[i].find("Switzerland")
    if index != -1:
        suc_swisslist.append(suc_list[i])
        
#Create header for csv file
#Parse data
##extract all SUCs from PHP source code into a string list
from datetime import datetime
csv_header.append('Date')
now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")	
suc_swisslist_int.append(date_time)

index =0
for i in range(len(suc_swisslist)):
    index = 0 #reset index
    #◘search for new Supercharger entry
    index = suc_swisslist[i].find("</b>")
    csv_header.append(suc_swisslist[i][0:index] + ' Available')
    csv_header.append(suc_swisslist[i][0:index] + ' Total')
    index = suc_swisslist[i].find("<br>Total", index)
    suc_swisslist_int.append(int(suc_swisslist[i][index-2:index]))
    index = suc_swisslist[i].find("<br>Age", index)
    suc_swisslist_int.append(int(suc_swisslist[i][index-2:index]))


ev_logger.log_csv("Suc_Switzerland.csv", suc_swisslist_int, csv_header)
    
    
    

    


        



