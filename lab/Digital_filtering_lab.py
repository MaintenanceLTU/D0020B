# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 22:29:34 2019

@author: Johan
"""
import pandas as pd
import numpy as np
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt

plt.close('all')

#%%Inputs
gRange = XX #g-range of accelerometer
gStatic = XX #Axis parallel to gravity => gStatic = 1, otherwise 0
T = XX #Total time

fc = XX #Cut-off
fc2 = np.array([XX, XX]) #Cut-off
 
y = pd.read_excel('dataexp.xlsx',header=None).values

N = len(y) #Number of signal samples
fs = N/T #Sampling frequency
t = np.arange(0,N,1).reshape((N,1))/fs #Time vector


#%% Converting to m/s^2
k = XX #
m = X #
y = ( (-m+y)/k - 1) * 9.82


#%% Filter
B, A = signal.butter(3, fc2/(fs/2), 'bandpass')
yb_p = signal.lfilter(B,A,y,axis=0)

#%% Integration
yvel = integrate.cumtrapz(yb_p,t,axis=0,initial=0)
#yvel_bp = signal.lfilter(B,A,yvel)

ydisp = integrate.cumtrapz(yvel,t,axis=0,initial=0)


#%% Plotting
fig1, ax1 = plt.subplots()
ax1.plot(t,y,label='Original noisy signal')
ax1.plot(t,yb_p,'r',linewidth=1.5,label='Filtered signal');
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Acceleration [m/s^2]')
ax1.legend()
ax1.grid()

fig2, ax2 = plt.subplots()
ax2.plot(t,yvel);
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Velocity [m/s]')
ax2.grid()

fig3, ax3 = plt.subplots()
ax3.plot(t,ydisp*1000);
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Displacement [mm]')
ax3.grid()
