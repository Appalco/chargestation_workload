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

#define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def plot(x, y, labels, title):
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(rotation=90)
    ax.stackplot(x, y, labels=labels)
    ax.set_title(title)
    plt.legend()
    plt.xlabel("Date")
    ax.set_title(title)
    n = 96
    for index, ticks in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            ticks.set_visible(False)
    plt.show()
    return

def multiplot(x, y1, y2, y3, y4, labels, title):
    plt.figure(dpi=300)
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(rotation=90)
    ax.plot(x, y1, label=labels[0])
    ax.plot(x, y2, label=labels[1])
    ax.plot(x, y3, label=labels[2])
    ax.plot(x, y4, label=labels[3])
    plt.legend()
    plt.xlabel("Date")
    plt.xticks(rotation=90)

    ax.set_title(title)
    n = 96
    for index, ticks in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            ticks.set_visible(False)
    plt.show()
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


fastned = 'fastned.csv'
evPass = 'evPass.csv'
Plugnroll = 'Plugnroll.csv'
EcarUP = 'EcarUP.csv'

filename = EcarUP
  
data1 = pd.read_csv('fastned.csv')
data2 = pd.read_csv('evPass.csv')
data3 = pd.read_csv('Plugnroll.csv')
data4 = pd.read_csv('EcarUP.csv')


plot(data1['Date'], data1['Occupied'], ["Fastned Network 2x 4 CCS Plugs 350kW"], "Occupied Chargers")
plot(data2['Date'], data2['Occupied'], ["EvPass Network Switzerland"], "Occupied Chargers")
plot(data3['Date'], data3['Occupied'], ["Plug N Roll Network Switzerland"], "Occupied Chargers")
plot(data4['Date'], data4['Occupied'], ["eCarUp Network Switzerland"], "Occupied Chargers")
multiplot(data1['Date'], data1['Occupied'],  data2['Occupied'],  data3['Occupied'], data4['Occupied'], ["Fastned", "EvPass", "PlugNroll", "EcarUp"], "Occupied chargers")


#Calcuate network useage in % and plot
useage = [calculate_useage(data1), calculate_useage(data2), calculate_useage(data3), calculate_useage(data4) ]
useage_av = [moving_avg(calculate_useage(data1), 96), moving_avg(calculate_useage(data2), 96), moving_avg(calculate_useage(data3), 96), moving_avg(calculate_useage(data4), 96) ]
multiplot(data1['Date'], useage[0],  useage[1], useage[2], useage[3], ["Fastned", "EvPass", "PlugNroll", "EcarUp"], "Chargenetwork worload [%]")

x = np.linspace(0, useage_av[1].shape[0], useage_av[1].shape[0], endpoint=True, retstep=False, dtype=None, axis=0)
multiplot(x, useage_av[0],  useage_av[1], useage_av[2], useage_av[3], ["Fastned", "EvPass", "PlugNroll", "EcarUp"], "Network useage in % moving average per day")
cumulated_sessions = [calculate_sessions(data1), calculate_sessions(data2), calculate_sessions(data3), calculate_sessions(data4) ]

       
plot(data1['Date'], cumulated_sessions[0], ["Fastned Network"], "Cumulated charge sessions")
plot(data2['Date'], cumulated_sessions[1], ["EvPass Network"], "Cumulated charge sessions")
plot(data3['Date'], cumulated_sessions[2], ["Plug N Roll Network"], "Cumulated charge sessions")
plot(data4['Date'], cumulated_sessions[3], ["eCarUp Network"], "Cumulated charge sessions")
multiplot(data1['Date'], cumulated_sessions[0],  cumulated_sessions[1],  cumulated_sessions[2], cumulated_sessions[3], ["Fastned", "EvPass", "PlugNroll", "EcarUp"], "Cumulated charge sessions")

normalized_session1 = []
normalized_session2 = []
normalized_session3 = []
normalized_session4 = []
for i in data1['Date'].index:
    normalized_session1.append(float(cumulated_sessions[0][i]/float(data1['Available'].max())))
    normalized_session2.append(float(cumulated_sessions[1][i]/float(data2['Available'].max())))
    normalized_session3.append(float(cumulated_sessions[2][i]/float(data3['Available'].max())))
    normalized_session4.append(float(cumulated_sessions[3][i]/float(data4['Available'].max())))

multiplot(data1['Date'], normalized_session1, normalized_session2, normalized_session3, normalized_session4, ["Fastned", "EvPass", "PlugNroll", "EcarUp"], "Cumulated charge sessions divided by number of plugs of charge network")
print("done")