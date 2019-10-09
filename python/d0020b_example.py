# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:17:59 2019

@author: Johan
"""
import numpy as np

#%% Assginment / Variables
Temperature = 1  #assign an integer to variable called temperature
b = 'hello' #string
c = 1.0 #float
d = True #bool

# Aritmetic operations
#Temperature = Temperature + 1
Temperature += 1
#print(Temperature**2)

#%% list
my_first_list = [1,1,2.5,3,'hello']
my_first_list[2] #get the third position from the list

# dict
my_first_dict = {'Temperature' : 3.14, 'Date' : '2019-09-05',
                 'name' : 'Johan', 'age' : 41, 'hungry' : True}
my_first_dict['Temperature']

#%% Numpy library
temperature_values = [2.3, 4.5, 6.7, 1.1, 1.2]
len(temperature_values)

mean_temperature = np.mean(temperature_values)
std_temperature = np.std(temperature_values)

#%% Define your own function
def my_range(values):
    max_value = max(values)
    min_value = min(values)
    range_values = max_value-min_value
    return range_values
    
print(my_range(temperature_values))

#%% If / else

temperature_outside = 5

if temperature_outside>=20:
    print('It is warm outside')
elif temperature_outside>=0:
    print('It is pretty ok outside')
else:
    print('It is clold outside')
    
    
# Loop
# Two types of looping for/while

# How to loop items in a list
for T in temperature_values:
    print(T)
    
for n in range(0,len(temperature_values),1):
    print(n)
    print(temperature_values[n])
    

n = 0
while n<len(temperature_values):
    print(temperature_values[n])
    n += 1
    
    
#%% Assignment 1
import json
filename = 'weather_data.json'
myfile = open(filename, 'r')
data=json.loads(myfile.read())
