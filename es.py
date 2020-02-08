#!/usr/bin/env python
import numpy as np       # operations on numerical arrays
import pandas as pd
import pandas_profiling

import os as os
import sys
import datetime as dt
from   dateutil.parser import parse
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from es_analytics  import * # homegrown classes
from es_utils import *
import rsrch_questions as rq

#from matplotlib.colors import BoundaryNorm
#from matplotlib.ticker import MaxNLocator

results = []
#Sfilename = 'Data/DeviceSensing_24-Jan-2020.csv'
#Pfilename = 'Data/PhoneSensing_24-Jan-2020.csv'
Sfilename = 'Data/DeviceSensing_07-Feb-2020.csv'
Pfilename = 'Data/PhoneSensing_07-Feb-2020.csv'
 
desloc = 0
if not os.path.exists(Sfilename):
    print ("Can't find data file: {}".format(filename))
    quit()
if not os.path.exists(Pfilename):
    print ("Can't find data file: {}".format(filename))
    quit()

#
#  Data files are opened
#

# 
# read and process Sensor measurements (from instruments)
dataS = pd.read_csv(Sfilename,sep=',', engine='python') # '\s+' regexp for whitespace
dataS = dataS.fillna('') # empty cells become empty strings!

# 
# read and process Cell Phope measurements (from instruments)
dataP = pd.read_csv(Pfilename,sep=',', engine='python') # '\s+' regexp for whitespace
dataP = dataP.fillna('') # empty cells become empty strings!
#print(dataP.head)
#profile = pfr.ProfileReport(dataX, title='ES data Profiling Report')
#profile.to_file(output_file="env_data.html")
#quit()

if False:
    print('\n\n')
    print('Data frame columns: Sensor Devices')
    print(list(dataS.columns.values))
    print('Data frame columns: Cell Phones')
    print(list(dataP.columns.values))
    print('')
    quit()
#print('Unique Locations so far: ')
Slocations = sorted(list(dataS.Location.unique()))
Plocations = sorted(list(dataP.Location.unique())) 
B_locs = sorted(list(set(Slocations+Plocations)))
#print('combined location list:', len(B_locs))
#print(B_locs)
setup_location_list(B_locs) 


###############################
#
# Process command line (now that we know data characteristics)
#
    
if len(sys.argv) ==1:
    if(sys.argv[1] == 'StudentData'):
        desloc = -1
        unit = 'Student Data'
    desloc = 1
    unit = 'SPL'
elif len(sys.argv) == 3:
    try:
        desloc = int(sys.argv[1])
    except:
        print_help()
        db_error('Illegal location in command line: {} (must be an int)'.format(sys.argv[1]))
    if sys.argv[2] not in units:
        print_help()
        db_error('Illegal unit in command line: {}'.format(sys.argv[2]))
    desloc = int(sys.argv[1])
    unit = sys.argv[2]
else:
    print_help()
    quit()

if desloc >= 0:
    print ('Starting up with location {} and unit: {}'.format(desloc, unit))
    print (' Location {} is {}'.format(desloc, locations[desloc]))
#print(data.head)
rename_tags(dataP)   # give the measurement types more compact names ('SPL', 'LUX')
rename_tags(dataS)   # give the measurement types more compact names ('SPL', 'LUX')
#print(data.head)

# Remove Blake's test inputs  (userid 5555)
id_key = 'Your 4 digit ID' 
indexvalues = dataP[dataP[id_key]==5555].index
dataP.drop(indexvalues, inplace=True)
indexvalues = dataS[dataS[id_key]==5555].index
dataS.drop(indexvalues, inplace=True)

if desloc >=0:  
    locname = locations[desloc]  # convert from int to full string name
else:
    locname = 'All'
     
#
#        Select one or more research questions to analyze
#
#        (set if stmt to True)


if True:
#
#  Analyze student measurement numbers
#

    id_tag = 'Your 4 digit ID'
    
    set = 'Sensor'
    #set = 'Phone'
    
    if set == 'Phone':    
        data_set = dataP
        descrip = 'Phone data entries'
    elif set == 'Sensor':
        data_set = dataS
        descrip = 'Sensor data entries'
    else:
        print('Unknown data set selector: '+set)
        quit()
    nres = rq.StudentNumbers(data_set, descrip)
    print('result shape: {}'.format(nres.shape))
    print('id     # results')
    print( nres)
    n = len(nres.index)
    navg = nres.mean()
    nstd = nres.std()
    nmed = nres.median()
    print('{} students, avg # results: {:5.1f}  median: {:5.1f}'.format(n, navg,nmed))
     #
    #  histogram
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    values = nres.tolist()
    print('value count: ', len(values), '\n',values)
    ax = plt.hist(values,bins=15)
    titlestr = 'Student data collection rates: ' + descrip
    plt.title(titlestr)
    plt.ylabel('Number of students')
    print('Xlabel: ', unit+' values')
    plt.xlabel('N measurements')  
    plt.xlim([0,40]) 
    plt.ylim([0,10]) 
    #
    #  Add a normal distrib
    #
    Amp = 100 # make it look bigger
    xmax = 40
    es_plot_stat_bar(plt, 6.0, navg,nstd,lcolor='red')
    es_plot_norm_curve(plt, xmax, navg, nstd, Amp)
    plt.text(18, 8, '18 required measurements')
    es_plot_stat_bar(plt,9.0, 18, 5, lcolor='green')
    plt.grid(True)
        
if False:
    rq.StudentReport(dataP, 'Cell Phone (SPL/LUX all locs.)')
    rq.StudentReport(dataS, 'Instrument Measurements')
    
if False:
    # Are cell phone measurements differenct for Apple vs Android?
    rq.Dev_Difference(dataP, locname, unit)
    
if False:        
    #
    #  Are two measurement distributions statistically different?
    #  (apply the T-test)
    #print('Enter a location to compare with {}'.format(locname))
    #list_locations()
    #l2 = input('Location selection: (integer):')
    #l2 = int(l2)
    print('Enter a location to compare with {}'.format(locname))
    #('Cell Phone (1) or Instrument (0)?: ')
    loc2=locations[get_a_location()]
    #data = select_InstPhone('Phone',dataP, dataS)
    data = select_InstPhone('Inst',dataP, dataS)
    rq.Loc_Difference(data, locname, loc2, unit)

if False:
    #
    #  Make a basic histogram of measurements in a single location
    #
    sel_data = rq.MeasurementHisto(dataP,locname,'(Cell)',unit)     
    sel_data = rq.MeasurementHisto(dataS,locname,'(Inst)',unit)     

# show all graphs     
plt.show()
