# Mobile Alerts Sensors


# Please check <https://github.com/sarnau/MMMMobileAlerts> for a full reverse engineered spec of the Mobile Alerts sensors!



My reverse engineering efforts to read the ELV Mobile Alerts sensors from Python.

ELV is selling affordable weather sensors <http://www.elv.de/ip-wettersensoren-system.html>, which can be monitored via an iOS application. To allow that all data is transmitted via a gateway to a server, which the application can access. Sadly the protocol is not documented. I don't think anybody has documented the way the URL has been constructed, especially the MD5 hash over the first part of it.

This sample code integrates sensors into fhem and I wrote it for Mac OS X, but it should work on Linux, too.

To integrate the sensors into fhem, add the sensors to the iOS application and check if they show up. You need to note all sensor IDs. The ID is 6 bytes long and represented as a hexadecimal number. This same code supports sensors of type 2 (temperature only) and type 3 (temperature and humidity), which can be recognized via the first two characters of the ID.

You have to adjust the following things in the code:

* **sensors = ...** Here you have to add all sensors IDs as strings
* **downloadPath** This needs to be adjusted to point to the log folder of fhem.
* **vendorid** You might want to change the UUID to a new one (just run **uuidgen** from the terminal)

