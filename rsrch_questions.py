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
def StudentReport(ds,description):
    print('-0-0-0-0-0        GOT HERE')
    id_key = 'Your 4 digit ID'
    ids = ds[id_key].unique()
    print('{} students have made entries'.format(len(ids)))
    npts = []
    maxbin = 30
    for id in ids:
        n = len(ds[ds[id_key]==id])
        print('id: {:4} pts: {}'.format(id,n))   
        npts.append(n)
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)     
    ax = plt.hist(npts,bins=10, range=(0,maxbin))
    lastdate = str(ds.iloc[-1].Timestamp)[0:7]
    plt.title(lastdate+': Student Sample Generation: '+description)
    plt.xlabel('Number of Data Points')
    plt.ylabel('# of Students')
    plt.xticks(range(maxbin))
    #plt.yticks(10.0*range(10))
    plt.xlim([0,maxbin])
    plt.ylim([0,10])
    plt.yticks(range(10))
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
    
    #
    #  Make a basic histogram of measurements 
       #(single location)
    #
    #sel_data = MeasurementHisto(devApp,location,'(Apple iOS)',unit)     
    #sel_data = MeasurementHisto(devAnd,location,'(Android)',unit)     
    sel_data = DualMeasHisto(devApp, devAnd, location, 'Apple vs Android', unit)
    
    print('Difference for measurements at '+location)
    Difference(devApp,devAnd, 'iPhone', 'Android', unit)
#
#  Are two measurement distributions statistically different?
#  (apply the T-test)
#
#  dataset = Pandas dataframe
#  loc1,loc2, string names of locations
def Loc_Difference(dataset, loc1, loc2, unit):
    maxbin= unit_range(unit)
    d = dataset[dataset.Quantity==unit]    # select measurement
    dloc1 = d.query('Location=="'+loc1+'"') # two locations
    dloc2 = d.query('Location=="'+loc2+'"')
    Difference(dloc1,dloc2, loc1, loc2, unit)
    
    mcol = 'Measurement Value (db or lux)'
    #
    #  histogram
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    v1 = dloc1[mcol].tolist()
    v2 = dloc2[mcol].tolist()
    print('*(*(*(*(*    value counts: ', len(v1), len(v2))
    ax = plt.hist(v1,bins=10,range=(0,maxbin))
    ax = plt.hist(v2,bins=10,range=(0,maxbin))
    titlestr =unit + 'values: '+loc1+' vs. '+loc2
    plt.title(titlestr)
    plt.ylabel('Number of measurements')
    print('Xlabel: ', unit+' values')
    plt.xlabel(unit+' values')  
    plt.xlim([0,maxbin]) 
    plt.grid(True)

    
#
#  Find distrib of student results
#
#
def StudentNumbers(data_set, descrip):
    id_tag = 'Your 4 digit ID'
    ids = data_set[id_tag]
    return  ids.value_counts()
    #return ids.unique(), ids.nunique()
    return ids.groupby().count()
#
#  Use the T-test to determine if the mean measurement from two datasets is 
#    significantly different (p<=0.05).
#
def Difference(d1,d2,name1, name2, unit):
    mcol = 'Measurement Value (db or lux)'
    T,p = stats.ttest_ind(d1[mcol], d2[mcol],equal_var=True)
    m1 = d1[mcol].mean()
    sd1 = d1[mcol].std()
    m2 = d2[mcol].mean()
    sd2 = d2[mcol].std()
    n1 = len(d1.index)
    n2 = len(d2.index)
    min_size = 3
    if n1 < 3 or n2 < 3:
        print('\n\n Warning - too few data samples: {} {}'.format(n1,n2))
        quit()
    print(' \nMeasurement: '+unit)
    print('      {:^20}        vs.       {:^20} '.format(name1, name2))
    print('mean: {:^20.1f} {}    mean: {:^20.1f} {}      Diff: {:4.1f} {}'.format(m1,unit,m2,unit, m2-m1,unit))
    print('  sd: {:^20.1f} {}      sd: {:^20.1f} {} '.format(sd1,unit,sd2,unit))
    print('   n: {:^20d}            n: {:^20d}        '.format(n1,n2))
    
    print('T stat: {:4.2f}, P-value: {:6.3f}'.format(T,p))
    if (p < 0.05):
        print('The difference is SIGNIFICANT')
    else:
        print('The difference is NOT significant')
    print('')
    



#
#  Make a double histogram of two sets of measurements in a single location
#
def DualMeasHisto(dataset1, dataset2, location, info_str, unit):
    mcol = 'Measurement Value (db or lux)'
    maxbin = unit_range(unit)
        
    dloc1 = dataset1.query('Location=="'+location+'"')
    dloc2 = dataset2.query('Location=="'+location+'"')
    #print(dloc.head())
    #quit()
    dty1 = dloc1[dloc1.Quantity==unit]
    dty2 = dloc2[dloc2.Quantity==unit]
    #
    #  histogram
    nbins = 15
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    values = dty1[mcol].tolist()
    print('value count: ', len(values), '\n',values)
    ax = plt.hist(values,bins=nbins,range=(0,maxbin))
    values = dty2[mcol].tolist()
    print('value count: ', len(values), '\n',values)
    ax = plt.hist(values,bins=nbins,range=(0,maxbin),alpha=0.5)
    titlestr =unit + 'values: '+location+' '+info_str 
    plt.title(titlestr)
    plt.ylabel('Number of measurements')
    print('Xlabel: ', unit+' values')
    plt.xlabel(unit+' values')  
    plt.xlim([0,maxbin]) 
    plt.ylim([0,70])
    plt.grid(True)
 

#
#  Make a basic histogram of measurements in a single location
#
def MeasurementHisto(dataset, location, info_str, unit):
    mcol = 'Measurement Value (db or lux)'
    maxbin = unit_range(unit)
        
    dloc = dataset.query('Location=="'+location+'"')
    #print(dloc.head())
    #quit()
    dty = dloc[dloc.Quantity==unit]
    #
    #  histogram
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    values = dty[mcol].tolist()
    print('value count: ', len(values), '\n',values)
    ax = plt.hist(values,bins=10,range=(0,maxbin))
    titlestr =unit + 'values: '+location+' '+info_str 
    plt.title(titlestr)
    plt.ylabel('Number of measurements')
    print('Xlabel: ', unit+' values')
    plt.xlabel(unit+' values')  
    plt.xlim([0,maxbin]) 
    plt.ylim([0,70])
    plt.grid(True)
 
