import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas import Series
import scipy
import scipy.signal
import datetime as dt

# Load and prepare 1 year of data with empty samples filled.
fatwatch_data = pd.read_csv('data/fatwatch_data.csv', index_col=0, parse_dates=True)
weights = fatwatch_data.Weight
w1y = weights[:'06-2010'].resample('D', fill_method='pad')
w1y_data = np.array(w1y)
n = len(w1y)

# Construct a Gaussian filter and smooth the data
filt = scipy.signal.gaussian( 31, 4 )
filt /= sum(filt)
padded = np.concatenate((w1y_data[0]*np.ones(31//2), w1y_data, \
  w1y_data[n-1]*np.ones(31//2)))
smooth = np.convolve(padded, filt, mode='valid')
smooth = Series(smooth, index=w1y.index)
unsmooth = w1y_data - smooth
daily_delta = fatwatch_data.Weight[:'06-2010'].resample('D').diff()

# Build a DataFrame with all the values for one year
weight_data = DataFrame({'Weight': w1y, 'Smoothed': smooth, \
  'Smoothing Error': unsmooth, 'Daily Delta': daily_delta})
weight_data['Day of Week'] = weight_data.index.map(lambda row: row.weekday())
weight_data['Week Number'] = weight_data.index.map(lambda row: \
  row.isocalendar()[0:2])
  
dd_pad = DataFrame({'Daily Delta': weight_data['Weight'].diff(), \
  'Day of Week': weight_data['Day of Week']})
dd_pad = pd.pivot_table(dd_pad, rows='Day of Week', values='Daily Delta')
dd_clean_wks = pd.pivot_table(weight_data, cols='Day of Week', rows='Week Number', \
  values='Daily Delta').dropna().mean()
dd_clean_dys = pd.pivot_table(weight_data, cols='Day of Week', rows='Week Number', \
  values='Daily Delta').mean()
avg_dds = DataFrame({'Padded': dd_pad, \
  'Only Measured': dd_clean_dys, \
  'Clean Weeks': dd_clean_wks})
newindex = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
avg_dds.index = newindex
