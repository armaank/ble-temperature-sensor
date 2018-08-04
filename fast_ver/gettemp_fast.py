# written by armaan kohli
# gettemp_fast.py -- a program used to connect to ble thermistor devices and read the ble uart tx for many readings  

import os
import sys
import time
import struct
import subprocess
from bluepy import btle
import datetime

# list of device addresses, scanable via 'sudo hcitool lescan'
# scan for ble thermistor devices and add the mac address here
device_addr = [
	"HI:JD:ES:EO:DC:EP",
	"DE:E8:6B:D3:DC:A9", 
	"AB:CD:EF:GH:IJ:KL"
	]

BLE_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
BLE_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

now = datetime.datetime.now()

def write_temp(temp):
	with open("/home/pi/temp_log.csv", "a") as csvlog:
		csvlog.write("{0},{1}\n".format(now.strftime("%m-%d-%Y %H:%M"), str(temp))


class MyDelegate(btle.DefaultDelegate):
        def __init__(self):
                btle.DefaultDelegate.__init__(self)

        def handleNotification(self, cHandle, data):
                data = bytearray(data)
		fout.write(data)
		fout.write("\n")
		write_temp(data)  

for x in range(0,len(device_addr)):
	
	os.system("sudo hciconfig hci0 down")
	time.sleep(1)
	os.system("sudo hciconfig hcio up")
	time.sleep(1)	

	print ("connecting to %s ... " %(device_addr[x]))
	textout = open("/home/pi/temp_log.txt", "a")
	textout.write("\nconnecting to %s at " % device_addr[x])
	textout.write(now.strftime("%m-%d-%Y %H:%M")+"\n")

	csvout = open("/home/pi/temp_log.csv", "a")
	
	try:
		dev = btle.Peripheral(device_addr[x], "random")
		dev.setDelegate( MyDelegate() )
		print ("connected")
	
		service_uuid = btle.UUID(BLE_SERVICE_UUID)
                ble_service = dev.getServiceByUUID(service_uuid)

                uuidConfig = btle.UUID(BLE_CHARACTERISTIC_UUID)
                data_chrc = ble_service.getCharacteristics(uuidConfig)[0]
                data_chrc = data_chrc.valHandle + 1

                dev.writeCharacteristic(data_chrc, "\x01\x00")

                time.sleep(1.0) # Allow sensor to stabilise

		while True:
			try:
				if dev.waitForNotifications(1.0): # handleNotification was caled
					continue
			except: # in the case where the connection drops mid comms
				print ("disconnected")
				textout.write("disconnected\n")
				dev.disconnect()
				break
	except:
		print ("unable to connect, failed")
		textout.write("unable to connect, failed \n")
		continue
textout.close()
print ("finished with all devices")
sys.exit(0)

