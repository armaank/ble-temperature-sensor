# written by armaan kohli
# script to get temperature data and append it to a file for a raspberry pi(ideally all versions, idk yet (dongle))
# usage: python getdata.py <device MAC address>
# dependencies: python(duh), pexpect(4.2 or later), raspbian jessie (8), BlueZ (v5.43 or later), bluetoothctl


import pexpect
import time
import sys
import os

#function to transmform a hex string into a signed integer
#####
def hexToInt(hexstr)
	val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
	if ((val&0x8000==0x8000: # treat signed 16 bits
		val = -((val^0xffff)+1)
	return val
#####

DEVICE = "00:12:34:56:78:90" # default device MAC address: change to mac address determined from hci, etc

if len(sys.argv) == 2:
	DEVICE = str(sys.argv[1]) # gets device MAC address from terminal input
else:
	print("enter a valid MAC address for a device")
	sys.exit(1)

# run gatttool
child = pexpect.spawn("gatttool -I")

# connect to device
print("connecting to:"), 
print(DEVICE)

NOF_REMAINING_RENTRY = 3 # number of times the pi can attempt to make a connection  

while True:
	try:
		child.sendline("connect {0}".format(DEVICE))
		child.expect("connection successful", timeout=5) # might need to change timeout to 10 
	except pexpect.TIMEOUT:
		NOF_REMAINING_RETRY=NOF_REMAINING_RETRY-1
		if(NOF_REMAINING_RETRY>0):
			print("timeout, retry ...")
			continue
		else:
			print("timeout, giving up")
			break
	else:
		print("connected!")
		break

if NOF_REMAINING_RETRY >0:
	# unixTime = int(time.time()) gmt time, I think, may need changing
	systemTime = int(time.localtime())
	# open file
	file = open("data.csv", "a")
	if(os.path.getsize("data.csv")==0:
		file.write("device\ttime\ttemperature\n")
	file.write(DEVICE)
	file.write("t")
	file.write(str(systemTime)) 
	file.write("t")

	# reads temperature data from GATT hex handle
	child.sendline("char-read-hnd 0x43")
	# need change GATT number for nRF51822 that corresponds to temperature (from keil firmware or hardware?)
	child.expect("characteristic value/descriptor: ", timeout = 5)
	child.exepct("\r\n", timeout=5)
	print("temperature: "),
	print("child.before"),
	print(float(hexToInt(child.before[0:5]))/100)

	file.write(str(float(hextoInt(child.before[0:5]))/100))
	file.write("\t")
	
	file.write("\n")
	file.close()
	print("done")
	
	sys.exit(0)
else:
	print("failed")
	sys.exit(1)
