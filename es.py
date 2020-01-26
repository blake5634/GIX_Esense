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
Sfilename = 'Data/DeviceSensing_24-Jan-2020.csv'
Pfilename = 'Data/PhoneSensing_24-Jan-2020.csv'

#usage = '''
    #>es [location] [unit]
        #- location = integer code for measurement site
        #- unit  =   SPL or LUX
    #'''
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
#print('Unique Locations so far: ')
Slocations = sorted(list(dataS.Location.unique()))
#print('Sensor Locations so far: ',len(Slocations))
Plocations = sorted(list(dataP.Location.unique()))
#print('Cell Phone Locations so far: ',len(Plocations))
#for i in range(len(Plocations)):
    #print (i,Plocations[i],Slocations[i])
B_locs = sorted(list(set(Slocations+Plocations)))
#print('combined location list:', len(B_locs))
#print(B_locs)
setup_location_list(B_locs)
#print(Slocations) 


###############################
#
# Process command line (now that we know data characteristics)
#
    
if len(sys.argv) ==1:
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

print ('Starting up with location {} and unit: {}'.format(desloc, unit))
print (' Location {} is {}'.format(desloc, locations[desloc]))
#print(data.head)
rename_tags(dataP)   # give the measurement types more compact names ('SPL', 'LUX')
rename_tags(dataS)   # give the measurement types more compact names ('SPL', 'LUX')
#print(data.head)

locname = locations[desloc]  # convert from int to full string name
     
     
if True:
    rq.StudentReport(dataP)
    
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
    loc2=locations[get_a_location()]
    data = select_InstPhone('Phone',dataP, dataS)
    rq.Loc_Difference(data, locname, loc2, unit)

if False:
    #
    #  Make a basic histogram of measurements in a single location
    #
    sel_data = rq.MeasurementHisto(data,locname,unit)     

# show all graphs     
plt.show()
