# chargestation_workload
Read live data from https://www.admin.ch/gov/de/start/dokumentation/medienmitteilungen.msg-id-76512.html

To generate data create a cronjob to log data at least every 15 minutes:

``` bash
0 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
0 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
5 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
5 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
10 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
10 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
15 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
15 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
20 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
20 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
25 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
25 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
30 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
30 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
35 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
35 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
40 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
40 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
45 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
45 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
50 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
50 * * * * cd /home/pi/chargestation_workload; python3 teslalogger_readphp_suc_status.py
55 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py
55 * * * * cd /home/pi/chargestation_workload; python3 Json_read_charge.py´´´

