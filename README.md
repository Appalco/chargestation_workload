# Json_read_charge.py

Read live data from ich-tanke-strom.ch
Dataset: https://opendata.swiss/dataset/ladestationen-fuer-elektroautos/resource/4d467a51-0bc9-48ce-aa2a-3d3bcaa7e7e9 
The script download the JSON stream and store the data from the five biggest operator into a csv file.

Execute the script as a cronjob to log data continously (every 15 minutes):

```bash
0 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
15 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
30 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
45 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
```

# plot_data.py
Search for the above generated csv files and plot some statistics

# teslalogger_readphp_suc_status.py
Log SuC data from teslalogger.de (experimental)




