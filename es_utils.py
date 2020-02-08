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


def get_a_location():
    list_locations()
    l2 = input('Location selection: (integer):')
    l2 = int(l2)
    return l2

def unit_range(unit):   
    if unit == 'SPL':
        maxbin = 150  # hearing damage
    elif unit == 'LUX':
        #maxbin = 1000 * (1+ int(dty['Measurement Value (db or lux)'].max() / 1000.0))
        maxbin = 1000
    return maxbin

# print debugging info
def print_deb(flag, string):
    if flag:
        print(string)
        
def db_error(str):
    print('\nError: '+str+'\n')
    quit()
    
    
def list_locations():
    print('refer to {} locations by number:'.format(len(locations)))
    for i,l in enumerate(locations):
        print(i, '  ', l)

def print_help():
    intro = '''
    A program to analyze data from the GIX MSTI T512 Environmental Sensing Lab.
    '''
    usage = '''
    >python3 es.py [location] [unit]
        - location = integer code for measurement site
        - unit  =   "SPL" or "LUX" (no quotes)
    '''
    
    print(intro)
    print(usage)
    list_locations()

def select_InstPhone(name, dP, dS):
    print ('Selecting Data source: ',name)
    if name=='Phone':
        return dP
    elif name.startswith('Inst'):
        return dS
    db_error('select_InstPhone: unknown source: '+name)
    
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
    name_map={'Sound pressure level, SPL (dBA)':'SPL', 'Light Flux':'LUX','Sound pressure level, SPL(dBA)':'SPL', 'Light Flux':'LUX'}
    for i,r in data.iterrows():
        data.at[i,'Quantity'] = name_map[r['Quantity']]
        
