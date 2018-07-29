import os
import glob
import time
import logging

from splunk_http_event_collector import http_event_collector
splunkHECKey = "7f75b2f2-2b0c-41c9-b9ac-beeec40f7410"
splunkHECHost = "192.168.2.11"
eventSender = http_event_collector(splunkHECKey, splunkHECHost)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

logging.basicConfig(filename='tempLog.log', level=logging.INFO)
while True:
    eventSender.sendEvent({
        "index": "main",
        "sourcetype": "Temperature",
        "source": "Apartment Temperature Reader",
        "host": "Pi",
        "event": { "Temp": read_temp() }
    })
    
    time.sleep(1) # reading takes about 1 sec