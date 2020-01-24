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
filename = 'Data/SensingResponses_23-Jan-2020.csv'

#usage = '''
    #>es [location] [unit]
        #- location = integer code for measurement site
        #- unit  =   SPL or LUX
    #'''
desloc = 0
if not os.path.exists(filename):
    print ("Can't find data file: {}".format(filename))
    quit()
else:
    
    data = pd.read_csv(filename,sep=',', engine='python') # '\s+' regexp for whitespace
    data = data.fillna('') # empty cells become empty strings!
    
    #profile = pandas_profiling.ProfileReport(data, title='ES data Profiling Report')
 # can output to file...
# profile.to_file(outputfile="/tmp/myoutputfile.html")
    
    #profile = pfr.ProfileReport(data, title='ES data Profiling Report')
    #profile.to_file(output_file="env_data.html")
    #quit()
    print('Data frame columns: ')
    print(list(data.columns.values))
    
    print('Unique Locations so far: ')
    locations = sorted(list(data.Location.unique()))
    print(locations)
    setup_location_list(locations)
    print_help()
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

print ('Starting up with location {} and unit: {}'.format(desloc, unit))



#print(data.head)
rename_tags(data)
#print(data.head)
    
db_g0 = dataset(data)  
#as {} records'.format(desloc, len(db_g0.df.index)))

## also create custom db's for each grp
#db_g1 = db_g0.select_group(1)
#db_g2 = db_g0.select_group(2)

## descriptive string
#gdesc = 'ALL Patients'
#db_selected = db_g0
#if desloc == 1:
    #gdesc = 'BEFORE 1-Feb-2014'
    #db_selected = db_g1
#if desloc == 2:
    #gdesc = 'AFTER 1-Feb-2014'
    #db_selected = db_g2
    
    

if True:
    locname = locations[desloc]
    sel_data = rq.MeasurementHisto(db_g0.df,locname,unit)
    #sel_data = rq.MeasurementHisto(db_g0.df,locname,'LUX')
    
     
    plt.show()
