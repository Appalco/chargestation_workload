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
import ev_logger as ev_logger
# Importing the statistics module 
import statistics 

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

def calculate_sessions(occupied, available):
    counter = 0
    charge_sessions_array = []
    for i in range(1, len(occupied)) :
        #calculate difference between current and next samples
        #if more chargers are occupied a session has started
        #try to ignore API errors, if spikes are too big or avaible=0 means multiple station were offline on last download
        #this is just a rough gess. Monitoring data precise is 
        #data for PlugNroll, Swisscharge, easy4you is bad quality (API offline for several hours, dropout etc.)
        diff =  occupied[i] - occupied[i-1]
        if diff > 0 and diff < 24:
            counter +=  diff
        charge_sessions_array.append(counter)
    charge_sessions_array.append(counter)
    return charge_sessions_array

def calculate_useage(Occupied, Available):
    useage = []
    #convert to lists
    for i in Occupied.index:
            useage.append(100 * Occupied[i] / (Available[i]+Occupied[i])) 
    return useage


  
data1 = pd.read_csv('Suc_Switzerland.csv')

   

#calculate used connecter instead available
labels = []
labels.append( "Dietikon, Switzerland")
labels.append( "Dietlikon, Switzerland - Erlenweg")
labels.append( "Affoltern, Switzerland")
labels.append( "Obfelden, Switzerland")
labels.append( "Maienfeld, Switzerland")

label_occupied = " Occupied"
label_available = " Available"

last48hrs = 192

plot(data1['Date'], data1['Dietikon, Switzerland Occupied'], ["SuC Dietikon"], "Occupied Suc Stalls", 96)
plot(data1['Date'], data1['Dietlikon, Switzerland - Erlenweg Occupied'], ["SuC Dietlikon"], "Occupied Suc Stalls", 96)
plot(data1['Date'], data1['Affoltern, Switzerland Occupied'], ["SuC Affoltern"], "Occupied Suc Stalls", 96)
plot(data1['Date'], data1['Obfelden, Switzerland Occupied'], ["SuC Obfelden"], "Occupied Suc Stalls", 96)
plot(data1['Date'], data1['Maienfeld, Switzerland Occupied'], ["SuC Maienfeld"], "Occupied Suc Stalls", 96)

multiplot(data1['Date'], data1['Dietikon, Switzerland Occupied'],  data1['Dietlikon, Switzerland - Erlenweg Occupied'],  data1['Affoltern, Switzerland Occupied'], data1['Obfelden, Switzerland Occupied'],  data1['Maienfeld, Switzerland Occupied'], ["Dietikon", "Dietlikon", "Affoltern", "Obfelden", "Maienfeld"], "Occupied chargers", 96)
multiplot(data1['Date'][len(data1)-last48hrs:len(data1)-1], data1['Dietikon, Switzerland Occupied'][len(data1)-last48hrs:len(data1)-1],  data1['Dietlikon, Switzerland - Erlenweg Occupied'][len(data1)-last48hrs:len(data1)-1],  data1['Affoltern, Switzerland Occupied'][len(data1)-last48hrs:len(data1)-1], data1['Obfelden, Switzerland Occupied'][len(data1)-last48hrs:len(data1)-1],  data1['Maienfeld, Switzerland Occupied'][len(data1)-last48hrs:len(data1)-1], ["Dietikon", "Dietlikon", "Affoltern", "Obfelden", "Maienfeld"], "Occupied chargers last 48hrs", 8)

# #Calcuate network useage in % and plot
useage = [calculate_useage(data1[labels[0] + label_occupied], data1[labels[0] + label_available]),
          calculate_useage(data1[labels[1] + label_occupied], data1[labels[1] + label_available]),
          calculate_useage(data1[labels[2] + label_occupied], data1[labels[2] + label_available]),
          calculate_useage(data1[labels[3] + label_occupied], data1[labels[3] + label_available]),
          calculate_useage(data1[labels[4] + label_occupied], data1[labels[4] + label_available])]

moving_average = [moving_avg(useage[0], 96), moving_avg(useage[1], 96), moving_avg(useage[2], 96), moving_avg(useage[3], 96), moving_avg(useage[4], 96)]
x = np.linspace(0, moving_average[0].shape[0], moving_average[0].shape[0], endpoint=True, retstep=False, dtype=None, axis=0)
          
multiplot(data1['Date'], useage[0], useage[1], useage[2], useage[3], useage[4], [labels[0], labels[1], labels[2], labels[3], labels[4]], "Useage SuC Stalls", 96)
multiplot(x, moving_average[0], moving_average[1], moving_average[2], moving_average[3], moving_average[4], [labels[0], labels[1], labels[2], labels[3], labels[4]],  "Moving average Useage SuC Stalls", 96)

cumulated_sessions = []
cumulated_sessions.append(calculate_sessions(data1[labels[0] + label_occupied], data1[labels[0] + label_available]))
cumulated_sessions.append(calculate_sessions(data1[labels[1] + label_occupied], data1[labels[1] + label_available]))
cumulated_sessions.append(calculate_sessions(data1[labels[2] + label_occupied], data1[labels[2] + label_available]))
cumulated_sessions.append(calculate_sessions(data1[labels[3] + label_occupied], data1[labels[3] + label_available]))
cumulated_sessions.append(calculate_sessions(data1[labels[4] + label_occupied], data1[labels[4] + label_available]))


multiplot(data1['Date'], cumulated_sessions[0],  cumulated_sessions[1],  cumulated_sessions[2], cumulated_sessions[3], cumulated_sessions[4], labels, "Cumulated charge sessions", 96)

# normalized_session1 = []
# normalized_session2 = []
# normalized_session3 = []
# normalized_session4 = []
# normalized_session5 = []
# for i in data1['Date'].index:
#     normalized_session1.append(float(cumulated_sessions[0][i]/float(data1[labels[0] + label_occupied] + data1[labels[0] + label_occupied])))
#     normalized_session2.append(float(cumulated_sessions[1][i]/float(data1[labels[1] + label_occupied] + data1[labels[1] + label_occupied])))
#     normalized_session3.append(float(cumulated_sessions[2][i]/float(data1[labels[2] + label_occupied] + data1[labels[2] + label_occupied])))
#     normalized_session4.append(float(cumulated_sessions[3][i]/float(data1[labels[3] + label_occupied] + data1[labels[3] + label_occupied])))
#     normalized_session5.append(float(cumulated_sessions[4][i]/float(data1[labels[4] + label_occupied] + data1[labels[4] + label_occupied])))

# multiplot(data1['Date'], normalized_session1, normalized_session2, normalized_session3, normalized_session4, normalized_session5, labels, "Cumulated charge sessions divided by number of plugs of charge network")


session_perday = [
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[0]),
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[1]), 
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[2]),
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[3]), 
    ev_logger.calculate_session_per_day(data1['Date'], cumulated_sessions[4]) ]
                              
plot(session_perday[0][0], session_perday[0][1], [labels[0]], "Charge Sessions per Day", 1)
plot(session_perday[1][0], session_perday[1][1], [labels[1]], "Charge Sessions per Day", 1)
plot(session_perday[2][0], session_perday[2][1], [labels[2]], "Charge Sessions per Day", 1)
plot(session_perday[3][0], session_perday[3][1], [labels[3]], "Charge Sessions per Day", 1 )
plot(session_perday[4][0], session_perday[4][1], [labels[4]], "Charge Sessions per Day", 1 )
multiplot(session_perday[0][0],  session_perday[0][1],   session_perday[1][1],  session_perday[2][1],  session_perday[3][1],  session_perday[4][1], labels, "Charge Sessions per day", 1)



useage_perday = [
    ev_logger.calculate_useage_per_day(data1['Date'], useage[0]),
    ev_logger.calculate_useage_per_day(data1['Date'], useage[1]), 
    ev_logger.calculate_useage_per_day(data1['Date'], useage[2]),
    ev_logger.calculate_useage_per_day(data1['Date'], useage[3]), 
    ev_logger.calculate_useage_per_day(data1['Date'], useage[4]) ]
                              
multiplot(useage_perday[0][0],  useage_perday[0][1],   useage_perday[1][1],  useage_perday[2][1],  useage_perday[3][1],  useage_perday[4][1], labels, "Charge net useage workload per day[%]", 1)
