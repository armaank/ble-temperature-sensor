# written by armaan kohli
# manage.py - a program used to control when ble thermistor devices are polled

import os
import sys
import time
import subprocess
import datetime

import schedule

def run_script():
	subprocess.call("python ~/rcs/gettemp.py", shell=True)

schedule.every(5).minutes.do(run_script)
#scheulde.every().hour.do(run_script)
while True:
	schedule.run_pending()
	time.sleep(1)
