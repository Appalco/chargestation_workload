# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 14:02:37 2021

@author: widmer
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
# Importing the statistics module 
import statistics 
from statistics import mean
import ev_logger as ev_logger

#define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def plot(x, y, labels, title, ticks_n):
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(rotation=90)
    ax.stackplot(x, y, labels=labels)
    ax.set_title(title)
    plt.legend()
    plt.xlabel("Date")
    ax.set_title(title)
    for index, ticks in enumerate(ax.xaxis.get_ticklabels()):
        if index % ticks_n != 0:
            ticks.set_visible(False)
    plt.show()
    fig.savefig(title + '.png',  bbox_inches = "tight")
    return

def multiplot(x, y1, y2, y3, y4, y5, labels, title, ticks_n):
    plt.figure(dpi=300)
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(rotation=90)
    ax.plot(x, y1, label=labels[0])
    ax.plot(x, y2, label=labels[1])
    ax.plot(x, y3, label=labels[2])
    ax.plot(x, y4, label=labels[3])
    ax.plot(x, y5, label=labels[4])
    plt.legend()
    plt.xlabel("Date")
    plt.xticks(rotation=90)

    ax.set_title(title)
    n = 96
    for index, ticks in enumerate(ax.xaxis.get_ticklabels()):
        if index % ticks_n != 0:
            ticks.set_visible(False)
    plt.show()
    fig.savefig(title + '.png',  bbox_inches = "tight")
    return

def calculate_sessions(data):
    counter = 0
    charge_sessions_array = []
    for i in (data.index-1):
        #calculate difference between current and next samples
        #if more chargers are occupied a session has started
        #try to ignore API errors, if spikes are too big or avaible=0 means multiple station were offline on last download
        #this is just a rough gess. Monitoring data precise is 
        #data for PlugNroll, Swisscharge, easy4you is bad quality (API offline for several hours, dropout etc.)
        diff = data['Occupied'].iloc[i+1] - data['Occupied'].iloc[i]
        if diff > 0 and diff < 50 and data['Available'].iloc[i] != 0: 
            counter +=  diff
        charge_sessions_array.append(counter)
    return charge_sessions_array

def calculate_useage(data):
    useage = []
    #convert to lists
    Available = data['Available'].tolist() 
    Occupied = data['Occupied'].tolist() 
    Unknown = data['Unknown'].tolist() 
    Outofservice = data['Outofservice'].tolist() 
    for i in data.index:
        if(Available[i] != 0):
            useage.append(100 * Occupied[i] / (Available[i]+Occupied[i]+Unknown[i]+Outofservice[i]))
        else: 
            useage.append(0)    
    return useage

def calculate_useage(data):
    useage = []
    #convert to lists
    Available = data['Available'].tolist() 
    Occupied = data['Occupied'].tolist() 
    Unknown = data['Unknown'].tolist() 
    Outofservice = data['Outofservice'].tolist() 
    for i in data.index:
        if(Available[i] != 0):
            useage.append(100 * Occupied[i] / (Available[i]+Occupied[i]+Unknown[i]+Outofservice[i]))
        else: 
            useage.append(0)    
    return useage

def calculate_totalconnectors(data):
    total_connectors = []
    #convert to lists
    Available = data['Available'].tolist() 
    Occupied = data['Occupied'].tolist() 
    Unknown = data['Unknown'].tolist() 
    Outofservice = data['Outofservice'].tolist() 
    for i in data.index:
        total_connectors.append(Available[i]+Occupied[i]+Unknown[i]+Outofservice[i])
    return total_connectors



  
data1 = pd.read_csv('fastned.csv')
data2 = pd.read_csv('evPass.csv')
data3 = pd.read_csv('Plugnroll.csv')
data4 = pd.read_csv('EcarUP.csv')
data5 = pd.read_csv('Swisscharge.csv')

labels = ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"]

last48hrs = 192

ticks = 24*24*4
plot(data1['Date'], data1['Occupied'], ["Fastned 2x 4 CCS Plugs 350kW (Lenzburg + Suhr)"], "Occupied Chargers Fastned", ticks)
plot(data2['Date'], data2['Occupied'], ["EvPass Network Switzerland"], "Occupied Chargers EvPass", ticks)
plot(data3['Date'], data3['Occupied'], ["Plug N Roll Network Switzerland"], "Occupied Chargers Plug n Roll", ticks)
plot(data4['Date'], data4['Occupied'], ["eCarUp Network Switzerland (public)"], "Occupied Chargers eCarUp", ticks)
plot(data5['Date'], data5['Occupied'], ["Swisscharge"], "Occupied Chargers Swisscharge", ticks)
multiplot(data1['Date'], data1['Occupied'],  data2['Occupied'],  data3['Occupied'], data4['Occupied'],  data5['Occupied'], ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"], "Occupied chargers", ticks)
multiplot(data1['Date'][len(data1)-last48hrs:len(data1)-1], data1['Occupied'][len(data2)-last48hrs:len(data2)-1], data2['Occupied'][len(data2)-last48hrs:len(data2)-1],  data3['Occupied'][len(data3)-last48hrs:len(data3)-1],  data4['Occupied'][len(data4)-last48hrs:len(data4)-1], data5['Occupied'][len(data5)-last48hrs:len(data5)-1], ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"], "Occupied chargers last 48hrs", 8)


#Calcuate network useage in % and plot
useage = [calculate_useage(data1), calculate_useage(data2), calculate_useage(data3), calculate_useage(data4), calculate_useage(data5)  ]
useage_av = [moving_avg(calculate_useage(data1), 96), moving_avg(calculate_useage(data2), 96), moving_avg(calculate_useage(data3), ticks), moving_avg(calculate_useage(data4), ticks), moving_avg(calculate_useage(data5), ticks) ]
multiplot(data1['Date'], useage[0],  useage[1], useage[2], useage[3], useage[4], labels, "Charge net useage workload [%]", ticks)

x = np.linspace(0, useage_av[1].shape[0], useage_av[1].shape[0], endpoint=True, retstep=False, dtype=None, axis=0)
# multiplot(x, useage_av[0],  useage_av[1], useage_av[2], useage_av[3], useage_av[4], labels, "Charge net useage workload [%] moving average per day", 96)
cumulated_sessions = [calculate_sessions(data1), calculate_sessions(data2), calculate_sessions(data3), calculate_sessions(data4), calculate_sessions(data5) ]

       
multiplot(data1['Date'], cumulated_sessions[0],  cumulated_sessions[1],  cumulated_sessions[2], cumulated_sessions[3], cumulated_sessions[4], labels, "Cumulated charge sessions", ticks)

normalized_session1 = []
normalized_session2 = []
normalized_session3 = []
normalized_session4 = []
normalized_session5 = []
for i in data1['Date'].index:
    normalized_session1.append(float(cumulated_sessions[0][i]/float(data1['Available'].iloc[0] + data1['Occupied'].iloc[0 ] +  data1['Unknown'].iloc[0] + data1['Outofservice'].iloc[0])))
    normalized_session2.append(float(cumulated_sessions[1][i]/float(data2['Available'].iloc[0] + data2['Occupied'].iloc[0 ] +  data2['Unknown'].iloc[0] + data2['Outofservice'].iloc[0])))
    normalized_session3.append(float(cumulated_sessions[2][i]/float(data3['Available'].iloc[0] + data3['Occupied'].iloc[0 ] +  data3['Unknown'].iloc[0] + data3['Outofservice'].iloc[0])))
    normalized_session4.append(float(cumulated_sessions[3][i]/float(data4['Available'].iloc[0] + data4['Occupied'].iloc[0 ] +  data4['Unknown'].iloc[0] + data4['Outofservice'].iloc[0])))
    normalized_session5.append(float(cumulated_sessions[4][i]/float(data5['Available'].iloc[0] + data5['Occupied'].iloc[0 ] +  data5['Unknown'].iloc[0] + data5['Outofservice'].iloc[0])))

multiplot(data1['Date'], normalized_session1, normalized_session2, normalized_session3, normalized_session4, normalized_session5, labels, "Cumulated charge sessions divided by number of plugs of charge network", ticks)

#Calculate sessions per day

session_perday = [
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[0]),
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[1]), 
    ev_logger.calculate_session_per_day(data2['Date'], cumulated_sessions[2]),
    ev_logger.calculate_session_per_day(data3['Date'], cumulated_sessions[3]), 
    ev_logger.calculate_session_per_day(data4['Date'], cumulated_sessions[4]) ]
                              
plot(session_perday[0][0], session_perday[0][1], [labels[0]], "Charge Sessions per day", 30)
plot(session_perday[1][0], session_perday[1][1], [labels[1]], "Charge Sessions per day", 30)
plot(session_perday[2][0], session_perday[2][1], [labels[2]], "Charge Sessions per day", 30)
plot(session_perday[3][0], session_perday[3][1], [labels[3]], "Charge Sessions per day", 30 )
plot(session_perday[4][0], session_perday[4][1], [labels[4]], "Charge Sessions per day", 30 )
multiplot(session_perday[0][0],  session_perday[0][1],   session_perday[1][1],  session_perday[2][1],  session_perday[3][1],  session_perday[4][1], labels, "Charge Sessions per day", 30)



useage_perday = [
    ev_logger.calculate_useage_per_day(data1['Date'], useage[0]),
    ev_logger.calculate_useage_per_day(data1['Date'], useage[1]), 
    ev_logger.calculate_useage_per_day(data2['Date'], useage[2]),
    ev_logger.calculate_useage_per_day(data3['Date'], useage[3]), 
    ev_logger.calculate_useage_per_day(data4['Date'], useage[4]) ]
                              
multiplot(useage_perday[0][0],  useage_perday[0][1],   useage_perday[1][1],  useage_perday[2][1],  useage_perday[3][1],  useage_perday[4][1], labels, "Charge net useage workload per day[%]", 30)

#Plot number of total chargers per network
multiplot(data1['Date'], calculate_totalconnectors(data1), calculate_totalconnectors(data2), calculate_totalconnectors(data3), calculate_totalconnectors(data4), calculate_totalconnectors(data5), ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"], "Total chargers", ticks)
#Plot number of total chargers per network
multiplot(data1['Date'], data1['Unknown'], data2['Unknown'], data3['Unknown'], data4['Unknown'], data5['Unknown'], ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"], "Status unknown", ticks)
#Plot number of total chargers per network
multiplot(data1['Date'], data1['Outofservice'], data2['Outofservice'], data3['Outofservice'], data4['Outofservice'], data5['Outofservice'], ["Fastned", "EvPass", "PlugNroll", "EcarUp", "Swisscharge"], "Status Out of order", ticks)