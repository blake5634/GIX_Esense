#
#  Utility functions
#
import datetime as dt
from   dateutil.parser import parse
 
ZEROTIME = dt.timedelta(seconds=0)
ONEHOUR = dt.timedelta(0,0,0,0,0,1) # one hour
OLDTIME = parse('1-Jan-1960')
 
#locations = ['On a bus (while bus is stopped)', 'Starbucks at a table', 'In class (on writing desk)', 'In the car', 'your bed at night', 'Outdoors by GIX: Cloudy', 'Outdoors by GIX: Sunny', 'GIX Woodshop: No machines (SPL only)', 'GIX Woodshop: Table Saw cutting (lux on table top, SPL from operating position)',  'GIX Woodshop: Dust Collector  (SPL Only, measure from table saw operating pos.)', 'GIX Woodshop: Dust Collector  (SPL Only, measure from table saw operating pos.)', 'GIX Woodshop: Drill (SPL Only from omerating position)']
locations = []


units = ['SPL','LUX']

# print debugging info
def print_deb(flag, string):
    if flag:
        print(string)
        
def db_error(str):
    print('\nError: '+str+'\n')
    quit()

def print_help():
    intro = '''
    A program to analyze data from the GIX MSTI T512 Environmental Sensing Lab.
    '''
    usage = '''
    >es [location] [unit]
        - location = integer code for measurement site
        - unit  =   "SPL" or "LUX" (no quotes)
    '''
    
    print(intro)
    print(usage)
    print('refer to {} locations by number:'.format(len(locations)))
    for i,l in enumerate(locations):
        print(i, '  ', l)

def setup_location_list(locs):
    for l in locs:
        locations.append(l)
    #locations = locs.copy()
    print ('location list len: {}'.format(len(locations)))
        
def rename_tags(data):
    '''
    Replace long form names of measurement Quantity with 3-letter units
    for cleaner access queries.
    '''
    name_map={'Sound pressure level, SPL (dBA)':'SPL', 'Light Flux':'LUX'}
    for i,r in data.iterrows():
        data.at[i,'Quantity'] = name_map[r['Quantity']]
        
