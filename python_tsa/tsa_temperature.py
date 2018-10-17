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

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#%% Read csv data to pandas Dataframe
# Read timestamp, temperature and windspeed columns from csv-file
# Add missing values "-" to NaN
data = pd.read_csv('values_device_weather-station.csv',header=0,sep=',',na_values=["-"])

# Convert timestamp from ms to s and add as date index to DataFrame
data.index = pd.to_datetime(np.float64(data["timestamp"])/1000,unit='s')

#%% Plot temperature data
plt.figure()
plt.plot(data.temperature)
plt.title('Temperature measurement data')
plt.ylabel('Degree Celsius (°C)')
plt.show()

#%% Print descriptive statistics and plot histogram
print(data[['temperature','windspeed']].describe())

data[['temperature','windspeed']].hist()
plt.show()

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
    plt.plot(feature_data, label='Feature values')
    plt.plot(rolmean,label='Rolling mean')
    plt.plot(rolstd,label = 'Rolling std')
    plt.legend(loc='best')
    plt.title(('Rolling mean and std dev for window of %d %s' % (window,unit)))
    plt.show()

# Rolling analysis for 1 week window
rollinganalysis(feature_data,window=(24*7),unit='hour')

## Using resmaple function
plt.figure()
plt.plot(data.temperature.resample('1H').mean(), label='1 hour mean')
plt.plot(data.temperature.resample('1W').mean(),label='1 week mean')
plt.plot(data.temperature.resample('1W').std(),label = '1 week std')
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
y = feature_data.values
# Create time signal in days
x = np.cumsum(np.append(0,np.float64(np.diff(feature_data.index))/(1e9*60*60*24)))

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

print("Slope of the trend is %0.2f hours (p=%0.3f)" % (slope, p_value))
print("Goodness of fit: R2=%0.3f and StdError=%0.3f" % (r_value**2, std_err))

# define residuals
reg_resid = pd.Series(y-(slope*x+intercept),index=feature_data.index)

#Plot
plt.figure()
plt.plot(x,y,'--*',label='Data')
plt.plot(x,x*slope+intercept,label='Linear regression model')
#plt.legend(loc='best')
plt.title('Trend analysis')
#plt.show()

# Least squares using numpy
X = np.vstack([x, np.ones(len(x))]).T
res = np.linalg.lstsq(X, y)

# Least squares using statsmodel
X = np.vstack([x**2, x, np.ones(len(x))]).T #Quadratic model
results = sm.OLS(y,X).fit()
print(results.summary())

plt.plot(x,results.fittedvalues,label='Least square quadratic model')
plt.legend(loc='best')
plt.show()

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
    result = teststationarity(data_resid.values,regression='c')
    
    fig=plt.figure() 
    ax = fig.add_subplot(211)
    ax.plot(data_resid)
    plt.title(label)
               
    
    ax = fig.add_subplot(212)
    res=stats.probplot(data_resid.values,plot=ax)    
    plt.show()
       
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
    
    
residualanalysis(decomp.resid.dropna(),label='Residuals from seasonal decompose')
residualanalysis(reg_resid,label='Residuals from regression analysis')

#%% Pivot table and correlation analysis
feature_data = data['temperature'].resample('1h').mean()
feature_data = pd.DataFrame(feature_data.interpolate())

data_hour = list()
data_day = list()
d = 0
for t in feature_data.index:
    data_hour.append(t.hour)
    if t.hour==0:
        d+=1
    data_day.append(d)

feature_data['hour'] = np.array(data_hour)
feature_data['day'] = np.array(data_day)
data_piv = feature_data.pivot(index='day', columns='hour', values='temperature')        
data_corr = data_piv.corr()
