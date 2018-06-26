
import pexpect
import time

DEVICE = "00:11:22:33:55:66" # change device uuid

print("Hexiwear address:"),
print(DEVICE)

# run gatttool interactively
print("running gatttool...")
child = pexpect.spawn("gatttool -I")

# connecting to the device
print("connecting to "),
print(DEVICE)
child.sendline("connect {0}".format(DEVICE))
child.expect("connection successful", timeout=10)
print("connected")

# print 'press ctrl-c to quit'
# function to transform hex string into a signed integer
def hexStrToInt(hexstr):
	val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
	if ((val&0x8000)==0x8000): # treat signed 16bits
		val = -((val^0xffff)+1)
	return val
# while true

