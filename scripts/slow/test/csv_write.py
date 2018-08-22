from time import sleep, strftime, time

def csv_write(temp, name):
	with open("./temp2.csv", "a") as log:
		log.write("{0},{1},{2},{3}\n".format(strftime("%Y-%m-%d"),strftime("%H:%M:%S"),name,str(temp)))


temp = int(raw_input('Enter Temp Value:'))
name = raw_input('Enter Name:')
csv_write(temp, name)
print('temperatures: ',temp)
