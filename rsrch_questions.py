#!/usr/bin/env python
import numpy as np       # operations on numerical arrays
import pandas as pd
import scipy.stats as stats
import os as os
import sys
import datetime as dt
from   dateutil.parser import parse
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from es_analytics  import * # homegrown classes
from es_utils import * 


FIG_WINDOW_SIZE=(12,10)


#
#  Are two measurement distributions statistically different?
#  (apply the T-test)
def Difference(dataset, loc1, loc2, unit):
    mcol = 'Measurement Value (db or lux)'
    d = dataset[dataset.Quantity==unit]    # select measurement
    dloc1 = d.query('Location=="'+loc1+'"') # two locations
    dloc2 = d.query('Location=="'+loc2+'"')
    T,p = stats.ttest_ind(dloc1[mcol], dloc2[mcol],equal_var=True)
    m1 = dloc1[mcol].mean()
    m2 = dloc2[mcol].mean()
    print(' \nMeasurement: '+unit)
    print(' {:10} vs.  {:10} '.format(loc1, loc2))
    print('   {:4.1f} {}    {:4.1f} {} Diff: {:4.1f} {}'.format(m1,unit,m2,unit, m2-m1,unit))
    print('T stat: {:4.2f}, P-value: {:4.2f}'.format(T,p))
    if (p < 0.05):
        print('The difference is SIGNIFICANT')
    else:
        print('The difference is NOT significant')
    print('')
    



#
#  Make a basic histogram of measurements in a single location
#
def MeasurementHisto(dataset, location, unit):
    mcol = 'Measurement Value (db or lux)'

    dloc = dataset.query('Location=="'+location+'"')
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)     
    dty = dloc[dloc.Quantity==unit]
    
    ax = plt.hist(dty[mcol],bins=10)
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

    
