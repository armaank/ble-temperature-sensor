# written by armaan kohli
# python script that uses getdata.py to get temperature data from multiple devices
# usage: python getalldata.py

import subprocess

# list of devices
devices = [
	"00:12:34:56:78:90", # device MAC addresses in a list to iterate through, must be determined beforehand
	"11:22:33:44:55:66",
	"77:88:99:00:11:22",
	]

for x in range(0,len(devices)):
	cmd = "python getdata.py " + devices [x]	
	subprocess.call(cmd, shell=True)

print("finished all devices")
