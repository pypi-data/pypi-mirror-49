"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: Summer 2017

Function: retrieve time series of variables within a predefined space-time domain.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import db
import subset
from datetime import datetime, timedelta
import time


def fillGaps(ts_original, y_original, y_std_original, startDate, endDate, fmt, dt):
    y = np.array([])
    y_std = np.array([])
    ts = []    
    startDate = datetime.strptime(str(startDate), fmt)
    endDate = datetime.strptime(str(endDate), fmt)
    t = startDate
    i, ind = 0, 0
    while t<=endDate:                        
        ts.append(t)
        gap = False
        if ind >= len(ts_original):
            gap = True
        elif ts_original[ind] == ts[i]:
            y = np.append(y, y_original[ind])
            y_std = np.append(y_std, y_std_original[ind])
            ind += 1
        else:
            gap = True
            
        if gap:
            y = np.append(y, np.nan)
            y_std = np.append(y_std, np.nan)            
        t = t + timedelta(minutes=dt)
        i += 1
    return ts, y, y_std


def iterative(table, field, dt):
    table = table.lower()
    it = False
    if dt != 24*60:
        it = True
    #if table.find('tblWind'.lower()) != -1:
    #    it = True
    #if table.find('tblCHL_OI'.lower()) != -1:
    #    it = True   
    #if table.find('tblPisces'.lower()) != -1:
    #    it = True
    return it


def timeSeries_iterative(table, field, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fmt='%Y-%m-%d', dt=24*60):
    y = np.array([])
    y_std = np.array([])
    ts = []    
    startDate = datetime.strptime(startDate, fmt)
    endDate = datetime.strptime(endDate, fmt)
    t = startDate
    while t<=endDate:        
        ts.append(t)
        t1 = t
        t2 = t + timedelta(minutes=dt) + timedelta(seconds=-1)
        df = subset.spaceTime(table, field, t1, t2, lat1, lat2, lon1, lon2, depth1, depth2)  
        t = t + timedelta(minutes=dt)
        try:
            if len(df[field]) > 0:                
                tempY = np.nanmean(df[field])
            else:
                tempY = np.nan
        except:
            tempY = np.nan   

        if abs(tempY) > 1e30:       ## remove outliers (extremes)
            tempY = np.nan   
            
        y = np.append(y, tempY)

        try:
            if len(df[field]) > 0:
                tempY_std = np.nanstd(df[field])
            else:
                tempY_std = np.nan
        except:
            tempY_std = np.nan        

        if abs(tempY_std) > 1e30:       ## remove outliers (extremes)
            tempY_std = np.nan   

        y_std = np.append(y_std, tempY_std)
    return ts, y, y_std


def timeSeries(table, field, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fmt='%Y-%m-%d', dt=24*60):    
    if iterative(table, field, dt):
        ts, y, y_std = timeSeries_iterative(table, field, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fmt, dt)
    else:   
        df = subset.timeSeries(table, field, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2)

        if table.lower().find('tblseaflow') != -1:
            from plotCruise import resample
            df = resample(df, 'D', removeNAs=False)
            df[field+'_std'] = None

        if not db.isClimatology(table):
            ts, y, y_std = pd.to_datetime(df[df.columns[0]]), df[field], df[field+'_std']
            ts, y, y_std = fillGaps(ts, y, y_std, startDate, endDate, fmt, dt)
        else:    
            ts, y, y_std = df[df.columns[0]], df[field], df[field+'_std']
    return ts, y, y_std

