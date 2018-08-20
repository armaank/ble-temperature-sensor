from time import sleep, strftime, time

def csv_write(temp, name):
	with open("./temp2.csv", "a") as log:
		log.write("{0},{1},{2}\n".name, format(strftime("%Y-%m-%d %H:%M:%S"),str(temp),name ))


temp = int(input('Enter Temp Value:'))
name = input('Enter Name:')
csv_write(temp, name)
print('temperatures: ',temp)
