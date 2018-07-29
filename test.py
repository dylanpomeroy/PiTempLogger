import requests
import datetime

from splunk_http_event_collector import http_event_collector

key = "7f75b2f2-2b0c-41c9-b9ac-beeec40f7410"
host = "localhost"

testevent = http_event_collector(key, host)
testevent.popNullFields = True

payload = {}
payload.update({"index":"main"})
payload.update({"sourcetype":"Temperature"})
payload.update({"source":"Apartment Temperature Reader"})
payload.update({"host":"Pi"})
payload.update({"event":{ "Temp": 22.1}})

result = testevent.sendEvent(payload)