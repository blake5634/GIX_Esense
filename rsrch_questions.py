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

#########
#
#  Study how many treatments per day
#
def Trtms_BID(dataset, group_label):
    tpds = []
    for p in dataset.patients:
        trtmtct = 0
        days = set() # empty set of patient's treatment days
        for i, r in p.data.iterrows():
            action = r['action']
            result = r['result']
            ##print ('xxx ...   action: {} result:  {}'.format(action,result))
            dattim = parse(r['time'])
            days.add(dattim.day)  # keep track of the hospitalization days
            #acthour = int(dattim.time().hour) # 0-23 hrs
            #print_deb(DB,'{} at {}hrs'.format(action,acthour))
            #if action.startswith('Calcium Level') and not result.isspace():  # a TCa calcium test
                #lasttest = dattim
                #self.testsbyhour[acthour] += 1
                #if float(result) < Lo_Ca:
                    #self.lCa_byhour[acthour] += 1
                #if float(result) > Hi_Ca:
                    #self.hCa_byhour[acthour] += 1
            
            ## magic codes for Calcitrol / calium citrate
            if action == str(12932) or action == str(12306):  # a treatment
                trtmtct += 1 # count the treatments
        tpd = trtmtct/len(days)   # treatments per day
        tpds.append(tpd)
    npts = len(tpds) # number patients
    if npts != dataset.npat:
        print ('Somethings wrong with patient count')
        quit()
    print ('looked at {} patients'.format(npts))
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    bins = 10
    #maxbin = 8
    print('Max trtmts per day = {}'.format(max(tpds)))
    maxbin = 2 + int(max(tpds))
    w =100 * np.ones(len(tpds)) * 1.0/float(dataset.npat) # percent of patients
    ax = plt.hist(tpds,bins=bins,range=(0,maxbin),density=False, weights=w)
    d1, b = np.histogram(tpds,bins=bins,range=(0,maxbin),density=False, weights=w)
    d2, b  = np.histogram(tpds,bins=bins,range=(0,maxbin),density=False)
    print('=/=/=/=/=/=')
    print (tpds, len(tpds))
    print(d1, sum(d1))
    print(d2,sum(d2))
    #histo, binedges = np.histogram(tpds, bins=5, range=(0,3), density=True)
    #
    #  overall histogram
    plt.title('Ca or calcitrol treatments per day: '+group_label)
    plt.xlabel('number of treaments per day')
    plt.ylabel('percent of {} patients'.format(npts))
    plt.xticks(range(maxbin))
    #plt.yticks(10.0*range(10))
    plt.xlim([0,maxbin])
    plt.ylim([0,100])
    plt.grid(True)

def Basic_Data_Profile(dataset, group_label):
    npat = 0
    nrec = []
    for p in dataset.patients:
        npat += 1
        #print ('patient {} has {} events in the record'.format(p.pid, len(p.data.index)))
        nrec.append(len(p.data.index))
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    ax = plt.hist(nrec,bins=20,range=(0,150))
    print ('There are '+str(npat)+' patients.')
    #
    #  overall histogram
    plt.title('basic data profile: '+group_label)
    plt.xlabel('number of entries per patient')
    plt.ylabel('number of patients')
    plt.grid(True)
    #print (nrec)
    #
    #  zoomed in to small records
    fig2,ax2 = plt.subplots(figsize=FIG_WINDOW_SIZE)
    ax2 = plt.hist(nrec,bins=20,range=(0,20))
    plt.xlabel('number of entries per patient (expanded range 0-20)')
    plt.ylabel('number of patients')
    plt.title('basic data profile: '+group_label)
    plt.xticks(range(20))
    plt.yticks(range(5))
    plt.grid(True)
    
    #########
    #
    #  First and last treatment start dates
    tmax = parse('01-Jan-1800')
    tmin = parse('31-Dec-2099')
    for p in dataset.patients:
        tstart = parse(p.data.iloc[0].time)   # first time stamp
        if tstart < tmin:
            tmin = tstart
        if tstart > tmax:
            tmax = tstart

    print('First record start: ',tmin)
    print('Last record start:  ',tmax)
    
    
def Cumulative_Pop_inHosp(dataset,group_label):
    #
    #  Graph cumulative population in hospital
    
    ndays = 10
    npts = 10   
    
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    pop = []
    days = []
    LOSs = []  
    npat = 0
    for p in dataset.patients:
        p.getLOS()
        LOSs.append(p.comps['LOS']/24.0)  # hours to days
        npat += 1
    for i in range(10):   # duration
        popu = sum ([j > i for j in LOSs] ) # should be a count of pop in hospital on day i+1
        print(i, popu, popu/npat )
        pop.append(100.0* popu/npat)  # how many patients
        days.append(1.0+i)
    ax = plt.plot(days,pop) # plot actual population vs time
    #
    # crude LOS model
    # 
    ptct = pop[1]*1.7   # initial # of patients
    rate = 0.40     # %disch/day
    d = np.exp(np.log(rate)/(npts/ndays))  # 4th root of rate
    print ('d = {:4.2f}%'.format(100*d))
    y = np.zeros(npts)
    x = np.zeros(npts)
    for i in range(npts):
        x[i] = 1.0 + ndays*i/float(npts)
        y[i] = ptct
        ptct = ptct * (1-d)
    #ax.set(xlim(0,10),ylim=(0,60), xlabel='days',ylabel='patient population')
    plt.xlabel('days in Hospital (blue: data, orange: 40% per day model')
    plt.ylabel('% patient population ('+group_label+')')
    plt.title('Percent patients after N days: '+group_label)
    plt.xlim([0,10])
    plt.ylim([0,100])
    plt.plot(x,y)    # plot model
    plt.grid(True)
        
        
        
def LOS_Distrib(dataset,group_label):
    #
    #  Graph the length of stay  LOS
    #
    plt.figure(1,figsize=FIG_WINDOW_SIZE)
    ax = plt.gca() 
    
    ## get the LOS for each patient
    #cst = pd.DataFrame(columns=['patient','group','LOS'])
    #for p in dataset.patients:
        #d = {'patient':p.pid, 'group':p.group, 'LOS':}
        #cst.append(d,ignore_index=True)
    LOSs1 = []
    LOSs2 = []
    # get a dataset for each group (before after the prototcol date)
    db_g1=dataset.select_group(1)
    db_g2=dataset.select_group(2)
    # histograms for all groups
    n1 = len(list(set(db_g1.df['patient']))) # get # of patients in group via set() 
    n2 = len(list(set(db_g2.df['patient'])))
    print ('n1:{}  n2:{}'.format(n1,n2))
    for p in db_g1.patients:
        p.getLOS()
        LOSs1.append(p.comps['LOS']/24.0)  # hours to days
    for p in db_g2.patients:
        p.getLOS()
        LOSs2.append(p.comps['LOS']/24.0)  # hours to days
    print('....... # patients: {}, {}'.format(len(LOSs1),len(LOSs2)))

    g1_h, g1_bins = np.histogram(LOSs1, bins = 10, range=(0.0,10.0))
    g2_h, g2_bins = np.histogram(LOSs2, bins = 10, range=(0.0,10.0))
    g1_h = g1_h/n1
    g2_h = g2_h/n2
    w = (g1_bins[1]-g1_bins[0])/3 # bar width
    ax.bar(g1_bins[:-1],   g1_h, width=w, facecolor='cornflowerblue')
    ax.bar(g1_bins[:-1]+w, g2_h, width=w, facecolor='yellow')        
    maxdays=10
    xl = 'LOS (days) (Yellow-Post, Blue-Pre)'
    ax.set(xlim=(0,maxdays),ylim=(0,1.0),xlabel=xl,ylabel='Fraction of ALL patients ')
    plt.grid(True)
    #
    # stats
    nlt2 = 0
    nlt3 = 0
    nlt5 = 0
    for ls in LOSs1:  # union of lists
        l = int(ls)
        if l < 2:
            nlt2 += 1
        if l < 3:
            nlt3 += 1
        if l < 5:
            nlt5 += 1
    print('< 2days: {:4.2f} < 3days: {:4.2f} < 5days: {:4.2f}, '.format(nlt2/n1,nlt3/n1,nlt5/n1)+'Group 1')
    
    nlt2 = 0
    nlt3 = 0
    nlt5 = 0        
    for ls in LOSs2:  # union of lists
        l = int(ls)
        if l < 2:
            nlt2 += 1
        if l < 3:
            nlt3 += 1
        if l < 5:
            nlt5 += 1
    print('< 2days: {:4.2f} < 3days: {:4.2f} < 5days: {:4.2f}, '.format(nlt2/n2,nlt3/n2,nlt5/n2)+'Group 2')
    
    nlt2 = 0
    nlt3 = 0
    nlt5 = 0        
    for ls in LOSs1+LOSs2:  # union of lists
        l = int(ls)
        if l < 2:
            nlt2 += 1
        if l < 3:
            nlt3 += 1
        if l < 5:
            nlt5 += 1
    print('< 2days: {:4.2f} < 3days: {:4.2f} < 5days: {:4.2f}, '.format(nlt2,nlt3,nlt5)+'Both Groups')
            
def Time_Oper2Pth(dataset,group_label):
    #
    #   time between OPERATE and PTH test  (should be < 25min)
    #
    dataset.time_2_PTH()
    print('Time 2 PTH: {} points'.format(len(dataset.comps['time_2_PTH'])))
    print (dataset.comps['time_2_PTH'])
    vdat = []
    for x in dataset.comps['time_2_PTH']:
        if not np.isnan(x):
            vdat.append(float(x))
    #valid = ~np.isnan(dataset.comps['time_2_PTH'])
    #print(valid)
    #print(type(valid))
    #print(np.shape(valid))
    #vdat = list(dataset.comps['time_2_PTH'])[valid==True]
    print('there are {} valid times and {} without valid PTH data'.format(len(vdat), dataset.npat-len(vdat)))
    print('the max interval is {} min.'.format(np.max(vdat)))
        
    lt_25min = 0
    lt_2hr   = 0
    for t in vdat:
        if t < 25:
            lt_25min+=1
        if t < 120.0:
            lt_2hr+=1
    print('{} patients < 25min,  {} patients < 2hrs'.format(lt_25min,lt_2hr))
            
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    ax = plt.hist(vdat, bins=30,range=(-60,10000))
    a = plt.gca()
    a.set_ylim([0,20])
    plt.xlabel('Time from OPERATE to first PTH test (min.)')
    plt.ylabel('# of patients '+group_label)
    plt.grid(True)


def Test_Time_Distrib(dataset,group_label):
    #
    #    Plot dist of test times
    #
    dataset.tst_trtmt_times() # compute the treatments and tests by hour of day
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    x = range(24) # hrs in day
    tot_tests_per_pat = 0
    for t in dataset.testsbyhour:
        tot_tests_per_pat += t/dataset.npat
    print('Total Tests per patient: {:5.2f}'.format(tot_tests_per_pat)+group_label)
    print('tests with Lo Ca by hour: ')
    #for i,c in enumerate(dataset.lCa_byhour):
        #print (i, c)
    #print('tests with Hi Ca by hour: ')
    #for i,c in enumerate(dataset.hCa_byhour):
        #print (i, c)
    #quit()
    
    PERPATIENT = True
    plt.xlabel('Hour (Blue: All, Orange: Low Ca,  Green: Hi Ca.)')

    if PERPATIENT:
    # # of tests per patient per hour
        ax = plt.bar(x,dataset.testsbyhour/(dataset.npat))
        ax = plt.bar(x,(dataset.hCa_byhour+dataset.lCa_byhour)/ (dataset.npat))  # lo Ca results per patient 
        ax = plt.bar(x,dataset.hCa_byhour/ (dataset.npat))  # lo Ca results per patient 
        a = plt.gca()
        a.set_ylim([0,0.5])  # total # of tests per hour
        plt.ylabel('# of Total Calcium Tests/patient: '+group_label)
    else:
        #  Total # of tests
        ax = plt.bar(x,dataset.testsbyhour)  
        ax = plt.bar(x,(dataset.hCa_byhour+dataset.lCa_byhour))  # lo Ca results  (orange)
        ax = plt.bar(x,dataset.hCa_byhour)  # lo Ca results per patient  (green)
        a = plt.gca()
        a.set_ylim([0,30])  # total # of tests per hour
        plt.ylabel('# of Total Calcium Tests: '+group_label)
    plt.grid(True)



def Trtmt_Time_Distrib(dataset,group_label):
    #
    #   Plot distribution of treatment times during 24 hr day.
    #
    dataset.tst_trtmt_times() # compute the treatments and tests by hour of day
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    x = range(24) # hrs in day
    tot_trtmts_per_pat = 0
    for t in dataset.trtmtsbyhour:
        tot_trtmts_per_pat += t/dataset.npat
    print('Total Treatments per patient: {:5.2f}: '.format(tot_trtmts_per_pat)+group_label)
    ax = plt.bar(x,dataset.trtmtsbyhour/(dataset.npat))
    #ax.set(xlim(0,10),ylim=(0,60), xlabel='days',ylabel='patient population')
    plt.xlabel('Hour')
    plt.ylabel('# of Treatments/patient: '+group_label)
    #plt.xlim([0,10]) 
    a = plt.gca()
    a.set_ylim([0,2.0])
    #plt.ylim([0,3])
    #plt.plot(x,y)
    plt.grid(True)
    
    
    
def Ca_Scatter(dataset,group_label): # db is a dataset    
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)  # first a basic Ca result histogram
    
    dataset.getCaTrend()   # figure out caclium trends
        
    #[item[0] for item in lst] 
    x = [item[0] for item in dataset.comps['CaTrend'] ] #relative time
    y = [item[1] for item in dataset.comps['CaTrend'] ] #iCa


    # Ca test result histogram
    ax = plt.hist(y, bins=20,range=(5,10))
    plt.xlabel('Total Ca for: '+group_label)
    plt.ylabel('# of test results')
    plt.title('Distribution of Calcium Scores')
    plt.grid(True)
    plt.show()

    #
    #  prior to plot, figure out distribution in last 24 hrs prior to discharge
    #
    rt =  [item[0] for item in dataset.comps['CaTrend'] if item[0] > -24]
    rCa = [item[1] for item in dataset.comps['CaTrend'] if item[0] > -24]
    
    print('24hr Mean: {:4.2f}, SD: {:4.2f}, 10th%tile: {:4.2f}'.format(np.mean(rCa), np.std(rCa), np.percentile(rCa, 10) ) )
    #
    fig,ax = plt.subplots(figsize=FIG_WINDOW_SIZE)
    # scatterplot
    scatter = ax.scatter(x,y)
    #plt.legend([ax],['LOS'],numpoints=5)
    #x = [0,5]
    #y = x
    #plt.xlabel('# ionic Ca tests (color by LOS)')
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))   # new name for tick marks
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax.xaxis.set_major_locator(plt.MultipleLocator(24))
    #ax.set_ylim=((5, 10))
    
    # Now we're going to overplot a few patients as line graphs 
        
    ## Randy and Manny designated groups
    ## patient can only be in one group.
    #MDG_los1day = [1, 6, 9, 19, 21, 23, 26, 27, 29, 32, 36, 38, 40, 44, 45, 49]
    #MDG_los1_2days = [7, 8, 12, 13, 28, 31, 37, 39, 55, 56, 57]
    #MDG_neck_dissect = [2, 3, 11, 17, 24, 35, 43, 48, 51, 52,  54]
    #MDG_Interm = [ 10, 14, 20, 33, 42, 46, 47, 50, 53]
    #MDG_HighRisk = [ 4 5 15 16 18 22 25 30 34 41]

    #plist = MDG_HighRisk
    ##groupname = 'High Risk Patients'
    #plist = MDG_Interm
    #groupname = 'Intermediate Risk Patients'
    #plist = MDG_neck_dissect
    #groupname = 'Neck Dissection Patients'
    #plist = MDG_los1day
    #groupname = 'Patients with LOS of 1 day'
    plist = MDG_los1_2days
    groupname = 'Patients with LOS of 1-2 days' 
    for p in plist:
        for p_inst in dataset.patients:  # patient instance
            if p == p_inst.pid: 
                ptrend_x=[]
                ptrend_y=[]
                pcurr = p_inst     # get full patient data
                # get pairs of time-TCa from patient
                for p2 in pcurr.comps['CaTrend']:
                    ptrend_x.append(p2[0])
                    ptrend_y.append(p2[1])
                    plt.plot(ptrend_x,ptrend_y)
    plt.xlabel('Time before discharge (hours)')
    plt.ylabel('Total Ca '+group_label)
    plt.title('Trajectories for '+groupname)
    plt.grid(True)
    
    print('got here 2')
    
