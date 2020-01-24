import numpy as np       # operations on numerical arrays
import pandas as pd
import os as os
import sys
import datetime as dt
from   dateutil.parser import parse
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
 
from es_utils import *
import rsrch_questions as rq

FIG_WINDOW_SIZE = (12,12)
 
        
#########################################################################################################3
#
#         dataset() class  (not clear if needed yet)
#

class dataset():
    def __init__(self,data_frame):
        self.df = data_frame
        self.comps = {} 
         
