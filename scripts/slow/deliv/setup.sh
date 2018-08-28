# written by armaan kohli

#!/bin/sh
# install programs/dependencies 
sudo apt-get update
sudo apt-get install bluetooth -y
sudo apt-get install bluez -y 
sudo apt-get install python-pip -y 
sudo apt-get install libglib2.0-dev -y 
pip install bluepy 
pip install schedule 

clear
echo "starting now"
# run scripts
python ./rcs/manage.py

