# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 20:36:30 2018
@author: Johan Odelius, Luleå University of Technology
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from scipy import stats
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#%% Read csv data to pandas Dataframe
# Read timestamp, temperature and windspeed columns from csv-file
# Add missing values "-" to NaN
data = pd.read_csv('values_device_weather-station.csv',header=0,sep=',',na_values=['-'])

# Convert timestamp from ms to s and add as date index to DataFrame
data.index = pd.to_datetime(np.float64(data["timestamp"])/1000,unit='s')

#%% Plot temperature data
plt.figure()
data['temperature'].plot()
plt.title('Temperature measurement data')
plt.ylabel('Degree Celsius (°C)')
plt.show()

#%% Print descriptive statistics and plot histogram
print(data[['temperature','windspeed']].describe())

data[['temperature','windspeed']].hist()

#%% Examine stationarity using rolling mean and std
# resample the data to 1 hour mean value
feature_data = data.temperature.resample('1H').mean()

## Using rolling function 
# Interpolate for equally time samples
feature_data = feature_data.interpolate() 

def rollinganalysis(y,window=5,center=True,unit=None):
    rolmean = y.rolling(window=window,center=center).mean()
    rolstd = y.rolling(window=window,center=center).std()
    plt.figure()
    plt.plot(y, label='Feature values')
    plt.plot(rolmean,label='Rolling mean')
    plt.plot(rolstd,label = 'Rolling std')
    plt.legend(loc='best')
    plt.title(('Rolling mean and std dev for window of %d %s' % (window,unit)))
    plt.show()

# Rolling analysis for 1 week window
rollinganalysis(feature_data,window=(24*7),unit='hour')

## Using resmaple function
plt.figure()
data.temperature.resample('1H').mean().dropna().plot(label='1 hour mean')
data.temperature.resample('1W').mean().plot(label='1 week mean')
data.temperature.resample('1W').std().plot(label = '1 week std')
plt.legend(loc='best')
plt.title('Mean and std dev resample for different time periods')
plt.show()  
  
## Statistic test for evaluating stationarity
# Augmented Dickey-Fuller unit root test
def teststationarity(values,signlevel=0.05,regression='c'):
    print('Augmented Dickey-Fuller with regression=%s'%regression)
    result = adfuller(values,regression=regression)
    h = result[1]<signlevel
    if h:
        print('- Reject H0, data is stationary (p=%0.3f)'%result[1])
    else:
        print('- Data seems non-stationary (p=%0.3f)'%result[1])
    return h

result = teststationarity(feature_data.values,regression='c')
result = teststationarity(feature_data.values,regression='ct')

#%% Trend analysis
# Resample to 24 hour mean, this will remove seasonal effect of day and night
feature_data = data.temperature.resample('24H').mean()

# Remove NaN from data
feature_data = feature_data.dropna()

# Extract values from series
y = feature_data.values
# Create time signal in days
t = feature_data.index
x = (t-t[0])//np.timedelta64(1,'D')

# Least square fit (matrix implementation using numpy)
n = len(x)
X = np.vstack([np.ones(n), x]).T
param = np.matmul(np.linalg.inv(np.matmul(X.T,X)),np.matmul(X.T,y)) # Model parameters

yhat = np.matmul(X,param) # Estimated values
r = y-yhat # Residuals

# Goodness of fit
SStot = sum((y-np.mean(y))**2)
SSres = sum(r**2)
Rsq = 1-SSres/SStot

df = n-2
# F-stat
SSreg = sum((yhat-np.mean(y))**2)
FStat = SSreg/(SSres/df)
pF = 1-stats.f.cdf(FStat,1,df)

# t-stat
SSx = sum((x-np.mean(x))**2)
SE = np.array([np.sqrt(SSres/df*(1/n+np.mean(x)**2/SSx)),np.sqrt(SSres/df/SSx)])
tStat = (param-np.array([0,0]))/SE
p = (1-stats.t.cdf(abs(tStat),df))*2

print('--- Least square fit and regression analysis  -----')
print('Estimated parameters: [%.1f,%.2f]' % tuple(param))
print('F-statistics: %.1f (p=%.3f)' % (FStat, pF))
print('Slope of the trend is %.2f deg/days (p=%.3f)' % (param[1], p[1]))
print('Goodness of fit: R2=%.3f' % (Rsq))
print('---------------------------------------------------')


# Least squares using numpy (equal to scipy.linalg.lstsq)
X = np.vstack([x, np.ones(len(x))]).T
coef, resid,_,_ = np.linalg.lstsq(X, y)

# Plot
# New figure with two subplots
fig, (ax1, ax2) = plt.subplots(2,1)
# Plot data and model
ax1.plot(x, y, 'o', label='Data')
ax1.plot(x, coef[0]*x + coef[1], label='Fitted line')
ax1.set_title('np.linalg.lstsq')
ax1.legend(loc='best')

# Plot residuals
ax2.plot(x, r, '*', label='Residuals')
ax2.set_title('Residuals')


# Linear regression (using scipy stats library)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

print('--------- scipy stats linear regression -----------')
print('Slope of the trend is %0.2f deg/days (p=%0.3f)' % (slope, p_value))
print('Goodness of fit: R2=%0.3f and StdError=%0.3f' % (r_value**2, std_err))
print('---------------------------------------------------')

# compute residuals
reg_resid = pd.Series(y-(slope*x+intercept),index=feature_data.index)

#Plot
# New figure with two subplots
fig, (ax1, ax2) = plt.subplots(2,1)
# Plot data and model
ax1.plot(x,y,'o', label='Data')
ax1.plot(x,x*slope+intercept,label='Linear regression model')
ax1.set_title('stats.linregress')
ax1.legend(loc='best')
# Plot residuals
ax2.plot(x, reg_resid, '*', label='Residuals')
ax2.set_title('Residuals')

# Regression using statsmodel OLS (Fit a linear model using Ordinary Least Squares)
X = np.vstack([x, np.ones(len(x))]).T
results = sm.OLS(y,X).fit()
print(results.summary())

# Plot
# New figure with two subplots
fig, (ax1, ax2) = plt.subplots(2,1)
# Plot data and model
ax1.plot(x,y, 'o', label='Data')
ax1.plot(x, results.fittedvalues,label='Linear regression model')
ax1.set_title('statsmodels OLS')
ax1.legend(loc='best')
# Plot residuals
ax2.plot(x, results.resid, '*', label='Residuals')
ax2.set_title('Residuals')


#%% Decomposition example
feature_data = data['temperature'].resample('1H').mean()
feature_data = feature_data.interpolate()
decomp = seasonal_decompose(feature_data, model='additive')
decomp.plot()
plt.show()

#%% Residual analysis
def residualanalysis(data_resid,label='Residuals'): 
    print(label)
    #Augmented Dickey-Fuller unit root test
    _ = teststationarity(data_resid.values,regression='c')
    
    # Plot residuals    
    fig=plt.figure() 
    ax = fig.add_subplot(211)
    ax.plot(data_resid)
    plt.title(label)
               
    # Plot normal prob plot
    ax = fig.add_subplot(212)
    _ = stats.probplot(data_resid.values,plot=ax)    
    # plt.show()
       
    #k2,p=stats.normaltest(data_resid)
    
    # Anderson darling test    
    print('Anderson Darling test for normality')
    r = stats.anderson(data_resid)    
    i = 2 #significan level of 0.05
    if r.statistic>r.critical_values[i]:
        print('Statistic: %.3f p<%.2f' % (r.statistic,r.significance_level[i]/100))        
        print('Fail to reject H0, data is normal')
    else:
        print('Statistic: %.3f p>%.2f' % (r.statistic,r.significance_level[i]/100))        
        print('Can reject H0, data is not normal')
    
    
# residualanalysis(decomp.resid.dropna(),label='Residuals from seasonal decompose')
residualanalysis(reg_resid,label='Residuals from regression analysis')

