from __future__ import division
import math

def conv_val(val):
	#print('Hello', person)

	R = 1023 / val - 1

	#print('resistance: ',R) 
	R = 10000 / R
	print('resistance: ',R)

	temp = R / 10000
	temp = math.log(temp)
	temp /= 3950
	temp += 1.0 / (25+273.15)
	temp = 1.0/temp
	temp -= 273.15
#	temp = temp*1.8 + 32

	return temp

R = int(input('Enter Thermistor Value:'))
out = conv_val(R)
print('temperatures: ',out)
