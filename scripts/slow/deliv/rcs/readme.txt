written by armaan kohli

Setup Instructions for Raspberry Pi portion

-download Raspbian-Stretch-Lite and use etcher.io to flah the OS to an SD card
-before ejecting the SD card, make an empty file named 'ssh', no extension, no content
-connect to the raspberry pi via Putty
-login with the following credentials: username:pi password:raspberry
-copy the folder 'rcs' into the ~ directory (/home/pi/)
-----using scp: 'scp -r rcs pi@<IP ADDR>:~' 
-change to the working directory rcs_scripts ('cd rcs')
-run the setup file ('./setup.sh')
-done!  
