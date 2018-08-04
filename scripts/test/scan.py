# written by armaan kohli
# scan.py -- a program used to scan for ble thermistor devices

import os
import sys
import time 
from bluepy import btle

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)
	
	def handleDiscovery(self, dev, isNewDev, isnNewData):
		if isNewDev:
			print("discovered device", dev.addr)
		elif isNewData:
			print("recieved new data from", dev.addr)

os.system("sudo hciconfig hci0 down")
time.sleep(1)
os.system("sudo hciconfig hci0 up")
time.sleep(1)

scanner = Scanner()

while True:
	
	print "scanning ..."
	print""
	for dev in devices
		print "[" + dev.addr + "]"
	
			for (adtype, desc, value) in dev.getScanData():
	
			if(desc=="Complete Local Name" and value=="BLE Thermistor"):
				print "|" + value + "|"

				break
		print ""
	time.sleep(1)
