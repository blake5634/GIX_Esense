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
#  How many students have entered data?
#
def StudentReport(ds):
    id_key = 'Your 4 digit ID'
    ids = ds[id_key].unique()
    print('{} students have made entries'.format(len(ids)))
    npts = []
    for id in ids:
        n = len(ds[ds[id_key]==id])
        print('id: {:4} pts: {}'.format(id,n))   
        npts.append(n)
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)     
    ax = plt.hist(npts,bins=10)
    plt.title('Student Sample Generation')
    plt.xlabel('Number of Data Points')
    plt.ylabel('# of Students')
    #plt.xticks(range(maxbin))
    #plt.yticks(10.0*range(10))
    #plt.xlim([0,maxbin])
    #plt.ylim([0,100])
    plt.grid(True)


#
#  Are measurements different between Android and iPhone??
#
def Dev_Difference(dataset, location, unit):
    apple = 'iPhone (all models)'
    android = 'Android (all models)'
    d = dataset[dataset.Quantity==unit]    # select measurement
    #d = d.query('Location=="'+location+'"') # select locations
    d = d[d.Location==location]
    phoneOStype = 'Your Phone'
    devApp = d[d[phoneOStype]==apple]
    devAnd = d[d[phoneOStype]==android]
    print('Difference for measurements at '+location)
    Difference(devApp,devAnd, 'iPhone', 'Android', unit)
#
#  Are two measurement distributions statistically different?
#  (apply the T-test)
#
#  dataset = Pandas dataframe
#  loc1,loc2, string names of locations
def Loc_Difference(dataset, loc1, loc2, unit):
    d = dataset[dataset.Quantity==unit]    # select measurement
    dloc1 = d.query('Location=="'+loc1+'"') # two locations
    dloc2 = d.query('Location=="'+loc2+'"')
    Difference(dloc1,dloc2, loc1, loc2, unit)
    
#
#  Use the T-test to determine if the mean measurement from two datasets is 
#    significantly different (p<=0.05).
#
def Difference(d1,d2,name1, name2, unit):
    mcol = 'Measurement Value (db or lux)'
    T,p = stats.ttest_ind(d1[mcol], d2[mcol],equal_var=True)
    m1 = d1[mcol].mean()
    m2 = d2[mcol].mean()
    n1 = len(d1.index)
    n2 = len(d2.index)
    if n1 < 5 or n2 < 5:
        print('\n\n Warning - too few data samples: {} {}'.format(n1,n2))
        quit()
    print(' \nMeasurement: '+unit)
    print(' {:^20} vs.  {:^20} '.format(name1, name2))
    print(' {:^20.1f} {}         {:^20.1f} {}                Diff: {:4.1f} {}'.format(m1,unit,m2,unit, m2-m1,unit))
    print(' {:^20}             {:^20}'.format('n='+str(n1),'n='+str(n2)))
    
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

    
