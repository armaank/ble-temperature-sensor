import math

R = int(input('Enter Thermistor Value: '))
#print('Hello', person)

#R = 10000*val / (1023 - val)

#print('resistance: ',R) 

temp = R / 10000
temp = math.log(temp)
temp /= 3950
temp += 1.0 / (25+273.15)
temp = 1.0/temp
temp -= 273.15


print('temperatures: ', temp)
