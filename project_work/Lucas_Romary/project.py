import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from scipy import stats
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import csv

import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)

# %% Read csv data to pandas Dataframe
data = pd.read_csv('projet.csv', header=0, sep=',', na_values=["-"])

#put data on variable
sulfurDioxyde = (data["field1"])
particles = (data["field3"])
monoxyde = (data["field2"])


def Average():
    i = 0
    j = 0
    k = 0
    value = 0.000
    value3 = 0.000

    while i < len(particles):
        value = value + (particles[i])
        i = i + 1

    value = value / len(particles)
    length = len(particles)-1
    print("The microparticle average is %0.1f pcs/0.01f between "% value + data.created_at[0] + " and " + data.created_at[length])

    while k < len(monoxyde):
        value3 = value3 + (monoxyde[k])
        k = k + 1

    value3 = value3 / len(monoxyde)
    length = len(monoxyde)-1
    print("The CO average is %0.1f ppm between "% value3 + data.created_at[0] + " and " + data.created_at[length]+"\n")


def maximumM():
    maximum = np.max(particles)
    a = [i for i, j in enumerate(particles) if j == maximum]
    b = a[0]
    print("The maximum peak for micro particles is %0.1f pcs/0.01cf at : "% maximum + data.created_at[b] +"\n")

def maximumCO():
    maximum = np.max(monoxyde)
    a = [i for i, j in enumerate(monoxyde) if j == maximum]
    b = a[0]
    print("The maximum peak for CO is %0.3f ppm at : "% maximum + data.created_at[b]+"\n")

def COAnalysis():
    for i in range(0,len(monoxyde)):
        if monoxyde[i]>100 and monoxyde[i]<200:
            print("Be careful the CO concentration is high (over 100ppm), time : " + data.created_at[i])
        if monoxyde[i] > 200 and monoxyde[i]<300:
            print("Be careful the CO concentration is very high (over 200ppm), time : " + data.created_at[i])
        if monoxyde[i] > 300:
            print("Be careful the CO concentration is huge (over 300ppm), your health could be affected, time : " + data.created_at[i])

def ParticlesAnalysis():
    for i in range(0,len(monoxyde)):
        if sulfurDioxyde[i]>20000 and sulfurDioxyde[i]<40000:
            print("Be careful the micro-particles concentration is quite high (over 20000 pcs/0.01cf), time : " + data.created_at[i])
        if sulfurDioxyde[i] > 40000 and sulfurDioxyde[i]<60000:
            print("Be careful the micro-particles concentration is  high (over 40000 pcs/0.01cf), time : " + data.created_at[i])
        if sulfurDioxyde[i] > 60000:
            print("Be careful the micro-particles concentration is huge (over 60000 pcs/0.01cf), your health could be affected, time : " + data.created_at[i])

def expositionCO() :
    compt = 0
    compt2 = 1
    length = len(monoxyde)-1

    for i in range(0, len(monoxyde)):
        if monoxyde[i]>100:
            compt = compt +1
    print("Carbon monoxide exposure time (>100ppm) : %0.1f min between " %compt + data.created_at[0] + " and " + data.created_at[length])
    num1 = len(monoxyde)-compt
    ratio = compt/num1
    print("the ratio of high concentration of CO is : ")
    print(ratio)
    print("\n")

def expositionP() :
    compt = 0
    length = len(particles)-1
    for i in range(0, len(particles)):
        if particles[i]>40000:
            compt = compt +1
    print("Particles exposure time (>40000 pcs/0.283ml) : %0.1f min between " %compt + data.created_at[0] + " and " + data.created_at[length])
    num1 = len(particles)-compt
    ratio = compt/num1
    print("the ratio of high concentration of particles is : ")
    print(ratio)
    print("\n")

plt.figure()
plt.plot(data.field3 )
plt.title('microparticles')
plt.ylabel('concentration ')
plt.show()

plt.figure()
plt.plot( data.field2 )
plt.title('CO')
plt.ylabel('concentration in ppm')
plt.show()

Average()

maximumM()
maximumCO()

expositionCO()
expositionP()








#
# def teststationarity(values, signlevel=0.05, regression='c'):
#     print('Augmented Dickey-Fuller with regression=%s' % regression)
#     result = adfuller(values, regression=regression)
#     h = result[1] < signlevel
#     if h:
#         print('- Reject H0, data is stationary (p=%0.3f)' % result[1])
#     else:
#         print('- Data seems non-stationary (p=%0.3f)' % result[1])
#     return h
#
#
# result = teststationarity(data.field2.values, regression='c')
# result = teststationarity(data.field2.values, regression='ct')
#
# # Linear regression
# y = data.field2
# x = data.entry_id
# slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# # Plot
# plt.figure()
# plt.plot(x, y, '--*', label='Data')
# plt.plot(x, x * slope + intercept, label='Linear regression model')
# plt.show()
#
#
# result = teststationarity(data.field3.values, regression='c')
# result = teststationarity(data.field3.values, regression='ct')
#
# # Linear regression
# y = data.field3
# x = data.entry_id
# slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# # Plot
# plt.figure()
# plt.plot(x, y, '--*', label='Data')
# plt.plot(x, x * slope + intercept, label='Linear regression model')
# plt.show()