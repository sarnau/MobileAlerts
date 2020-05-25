#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import pprint
import datetime
import hashlib
import time
import urllib.request

downloadPath = os.path.expanduser('~/fhem-5.7/log')
pp = pprint.PrettyPrinter()

sensors =  set(['021122334455',...,'031122334455'])

def parseJSON(jj):
    if not jj['success']:
        print('#%d %s' % (jj['errorcode'],jj['errormessage']))
        return
    for device in jj['result']['devices']:
        #pp.pprint(device)
        deviceTypeId = device['devicetypeid']
        deviceName = device['name']
        print('%s %s [%d] #%d %s' % 
                (
                    device['deviceid'],
                    deviceName,
                    device['lowbattery'],
                    len(device['measurements']),
                    datetime.datetime.fromtimestamp(device['lastseen']).strftime('%Y-%m-%d %H:%M:%S')
                )
        )
        year = -1
        month = -1
        logPath = ''
        for measurement in device['measurements']:
            idx = measurement['idx']
            transmitTime = datetime.datetime.fromtimestamp(measurement['c'])
            measurementTime = datetime.datetime.fromtimestamp(measurement['ts'])
            tx = measurement['tx']
            mm = measurement
            del mm['idx']
            del mm['c']
            del mm['ts']
            del mm['tx']

            if year != measurementTime.year or month != measurementTime.month:
                if len(logPath):
                    f = open(logPath, "w")
                    for d in sorted(data):
                        f.write('%s %s\n' % (d,data[d]))
                year = measurementTime.year
                month = measurementTime.month
                logPath = downloadPath + '/S_SENSOR_%s-%d-%02d.log' % (deviceName.upper().replace(' ','_'),year,month)
                data = {}
                try:
                    for line in open(logPath).readlines():
                        vals = line[:-1].split(' ')
                        data[' '.join(vals[:-1])] = vals[-1]
                except:
                    pass
            dataKey = measurementTime.strftime('%Y-%m-%d_%H:%M:%S') + ' SENSOR_' + deviceName.upper().replace(' ','_') + ' '
            if deviceTypeId == 2:
                data[dataKey + 'TEMP:'] = '%.1f' % (measurement['t1'])
            elif deviceTypeId == 3:
                data[dataKey + 'TEMP:'] = '%.1f' % (measurement['t1'])
                data[dataKey + 'FEUCHTIGKEIT:'] = '%.1f' % (measurement['h'])
            else:
                pp.pprint(mm)
        if len(logPath):
            f = open(logPath, "w")
            for d in sorted(data):
                f.write('%s %s\n' % (d,data[d]))


devicetoken = 'empty'				# defaults to "empty"
vendorid = '7be5c039-f650-439e-887f-f410b3c959db'	# iOS vendor UUID (returned by iOS, any UUID will do). Launch uuidgen from the terminal to generate a fresh one.
phoneid = 'Unknown'					# Phone ID - probably generated by the server based on the vendorid (this string can be "Unknown" and it still works)
version = '1.35'					# Info.plist CFBundleShortVersionString
build = '132'						# Info.plist CFBundleVersion
executable = 'Mobile Alerts'		# Info.plist CFBundleExecutable
bundle = 'de.synertronixx.remotemonitor'	# [[NSBundle mainBundle] bundleIdentifier]
lang = 'en'							# preferred language

request = "devicetoken=%s&vendorid=%s&phoneid=%s&version=%s&build=%s&executable=%s&bundle=%s&lang=%s" % (devicetoken,vendorid,phoneid,version,build,executable,bundle,lang)
request += '&timezoneoffset=%d' % 60		# local offset to UTC time
request += '&timeampm=%s' % ('true')		# 12h vs 24h clock
request += '&usecelsius=%s' % ('true')		# Celcius vs Fahrenheit
request += '&usemm=%s' % ('true')			# mm va in
request += '&speedunit=%d' % 0				# wind speed (0: m/s, 1: km/h, 2: mph, 3: kn)
request += '&timestamp=%s' % datetime.datetime.utcnow().strftime("%s")	# current UTC timestamp

requestMD5 = request + 'uvh2r1qmbqk8dcgv0hc31a6l8s5cnb0ii7oglpfj'	# SALT for the MD5
requestMD5 = requestMD5.replace('-','')
requestMD5 = requestMD5.replace(',','')
requestMD5 = requestMD5.replace('.','')
requestMD5 = requestMD5.lower()
requestMD5 = requestMD5.encode('utf-8')

m = hashlib.md5()
m.update(requestMD5)
hexdig = m.hexdigest()

request += '&requesttoken=%s' % hexdig

request += '&deviceids=%s' % ','.join(sensors)
#request += '&measurementfroms=%s' % ('0,' * len(sensors))
#request += '&measurementcounts=%s' % ('50,' * len(sensors))

http_header = {
                "User-Agent" : "remotemonitor/248 CFNetwork/758.2.8 Darwin/15.0.0",
                "Accept-Language" : "en-us",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "Host" : "www.data199.com:8080",
                }

# create an urllib.request opener()
opener = urllib.request.build_opener()

# create your HTTP request
req = urllib.request.Request('https://www.data199.com/api/v1/dashboard', request.encode('utf-8'), http_header)

# submit your request
while True:
    res = opener.open(req)
    parseJSON(json.loads(res.read()))
    print('-' * 40)
    time.sleep(10*60)	# wait for 10 minutes
