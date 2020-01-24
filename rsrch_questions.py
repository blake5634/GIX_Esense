#!/usr/bin/env python
import numpy as np       # operations on numerical arrays
import pandas as pd
import os as os
import sys
import datetime as dt
from   dateutil.parser import parse
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from es_analytics  import * # homegrown classes
from es_utils import * 


FIG_WINDOW_SIZE=(12,10)

def MeasurementHisto(dataset, location, unit):
    #unit = 'SPL'
    print ('MH: location: {} unit: {}'.format(location, unit))
    dloc = dataset.query('Location=="'+location+'"')
    #print(dloc)
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    x = []
    v = []
    #for i, r in d.iterrows():
        #x.append(i)
        #v.append(r['Location'])
    
    dty = dloc[dloc.Quantity==unit]
    ax = plt.hist(dty['Measurement Value (db or lux)'],bins=10)
    #
    #  overall histogram
    plt.title(unit + 'values: '+location)
    plt.xlabel('values')
    if unit == 'SPL':
        maxbin = 150  # hearing damage
    elif unit == 'LUX':
        maxbin = 1000 * (1+ int(dty['Measurement Value (db or lux)'].max() / 1000.0))
    #plt.ylabel('')
    #plt.xticks(range(maxbin))
    #plt.yticks(10.0*range(10))
    plt.xlim([0,maxbin])
    #plt.ylim([0,100])
    plt.grid(True)

    
