# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:09:01 2021

@author: widmer
"""

import ev_logger as ev_logger
    
def suc_list_to_csv(suc_list, filename):
    #Create header for csv file
    #Parse data
    ##extract all SUCs from PHP source code into a string list
    from datetime import datetime
    csv_header = []
    csv_header.append('Date')
    suc_list_int = []
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M")	
    suc_list_int.append(date_time)
    
    index = 0
    for i in range(len(suc_list)):
        index = 0 #reset index
        #◘search for new Supercharger entry
        index = suc_list[i].find("</b>")
        csv_header.append(suc_list[i][0:index] + ' Occupied')
        csv_header.append(suc_list[i][0:index] + ' Available')
        index =suc_list[i].find("Site Closed!") 
        if index != -1:
            #Found Site clodes string
            #Site is closed available 0
            suc_list_int.append(0)
            suc_list_int.append(0)
        else :
            index = suc_list[i].find("<br>Total")
            available = int(suc_list[i][index-2:index])
            index = suc_list[i].find("<br>Age", index)
            total = int(suc_list[i][index-2:index])
            #Now we want to log occupied and available connectors in csv
            suc_list_int.append(total-available)
            suc_list_int.append(available)                  
    ev_logger.log_csv(filename, suc_list_int, csv_header)
    return
    

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
suc_stringlist = []
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
        suc_stringlist.append(php_string[index_start+string_offset:index_end]) 
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
suc_norwaylist = []
suc_norwaylist_int = []
suc_swedenlist = []
suc_swedenlist_int = []


#Reduce data to Switzerland only
for i in range(len(suc_stringlist)):
    #◘search for Switzerland keyword
    index = suc_stringlist[i].find("Switzerland")
    index2 = suc_stringlist[i].find("Norway")
    index3 = suc_stringlist[i].find("Sweden")
    if index != -1:
        suc_swisslist.append(suc_stringlist[i])
    if index2 != -1:
       suc_norwaylist.append(suc_stringlist[i])
    if index3 != -1:
       suc_swedenlist.append(suc_stringlist[i])
        
suc_list_to_csv(suc_swisslist, "Suc_Switzerland.csv")
suc_list_to_csv(suc_norwaylist, "Suc_Norway.csv")
suc_list_to_csv(suc_swedenlist, "Suc_Sweden.csv")

# index = 0
# for i in range(len(suc_swisslist)):
#     index = 0 #reset index
#     #◘search for new Supercharger entry
#     index = suc_swisslist[i].find("</b>")
#     csv_header.append(suc_swisslist[i][0:index] + ' Available')
#     csv_header.append(suc_swisslist[i][0:index] + ' Total')
#     index = suc_swisslist[i].find("<br>Total", index)
#     suc_swisslist_int.append(int(suc_swisslist[i][index-2:index]))
#     index = suc_swisslist[i].find("<br>Age", index)
#     suc_swisslist_int.append(int(suc_swisslist[i][index-2:index]))


# ev_logger.log_csv("Suc_Switzerland.csv", suc_swisslist_int, csv_header)
    
    
    

    


        



