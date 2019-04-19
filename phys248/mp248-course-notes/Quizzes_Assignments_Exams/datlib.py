## Let's import our code from Lecture 8 (Simple Stats) and Lab 8.
## we'll modify it a little bit so it can grab the weather data from
## multiple directories.

## coml common weather dates.
## clean_dat crime stats
## vic_dict Victoria crime stats

import datetime as dt
import os as os
from operator import itemgetter
import collections as co
import fnmatch as fn    ## library for finding files using OS wildcards
import numpy as np
import json
import collections as co
import pprint as pp
import datetime as dt

print("datlib cwd", os.getcwd())

## directories containing the weather w.* subdirectories
sdp = ['Labs/L8.data', 'data']

## Build the list of directories of the weather files.
wsubdirs = sum( [[x+'/'+y for y in fn.filter(os.listdir(x), "w.*")] for x in sdp], [] )

## basic line formatting. This is used in the next code block.
## Code removes quotes and newlines, and splits along commas.
def fmtline(ln):
    PL = ln.translate({ord(c): None for c in '"\n'})
    PL = PL.split(",")
    return(PL)

## we will store the file data in a co.defaultdict(dict)
## format initDat["location"][date][dict key such as max temp, min temp, etc.] 

initDat = co.defaultdict(dict)

for wd in wsubdirs:
    files = fn.filter(os.listdir(wd), "eng-daily*.csv")
    for wdf in files:
        with open(wd+'/'+wdf, encoding='utf-8') as f:
            content = f.readlines()
            
            ## find line describing columns
            keylines = [i for i in range(len(content)) if 'date/time' in\
                        content[i].lower()]
            if len(keylines)!=1:
                print("Error: "+wd+'/'+wdf+" key error. ")
                () = () + 1
            
            ## find station data
            stnlines = [i for i in range(len(content)) if 'station name' in\
                        content[i].lower()]
            if len(stnlines)!=1:
                print("Error: "+wd+'/'+wdf+" stn name error. ")
                () = () + 1
                
            airpt = fmtline(content[stnlines[0]])[1]
            keys = fmtline(content[keylines[0]])
            ## get date/time index
            dti = [j for j in range(len(keys)) if 'date/time' in\
                   keys[j].lower()]
            if len(dti)!=1:
                print("Error: "+wd+'/'+wdf+' date/time idx. ')
                () = () + 1
            
            ## let's collect the data
            for i in range(keylines[0]+1, len(content)):
                ln = fmtline(content[i])
                ## convert date/time to python datetime object
                ln[dti[0]] = dt.datetime.strptime(ln[dti[0]], "%Y-%m-%d")
                
                initDat[airpt][ln[dti[0]]] = dict( [ (keys[j] , ln[j]) for j in\
                                                    range(len(keys)) if j != dti[0] ] ) 
                
'''              
## date gap check for initDat, i.e. report what (if any) days have missing weather data.
for A in initDat.keys():
    sd = sorted( initDat[A].keys() )
    print('First date: ',sd[0].date(), 'Final date: ', sd[-1].date())
    ID = sd[0]
    mD = []
    while ID<sd[-1]:
        ID += dt.timedelta(days=1)
        if ID not in initDat[A].keys():
            mD.append(ID)
    if (len(mD)>0):
        print("Missing dates: ", mD)
    else:
        print(sd[-1].date()-sd[0].date())'''

## list of keys we will have use for.
ncl = ['Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)',\
       'Total Rain (mm)', 'Total Snow (cm)', 'Total Precip (mm)']

## let's make sure all the max, min, mean, total rain, total snow, total precip floats are present
for A in initDat.keys():
    for k in ncl:
        am = 0
        for d in initDat[A].keys():
            if len(initDat[A][d][k])==0:
                am += 1
        #print('Airport: ', A, 'missing ', k, ' count ', am)

## merge dictionaries for the four cities

edmdict = dict()
caldict = dict()
vicdict = dict()
sasdict = dict()
for k in initDat.keys():
    if 'EDM' in k:
        edmdict.update(initDat[k])
    if 'CAL' in k:
        caldict.update(initDat[k])
    if 'VIC' in k:
        vicdict.update(initDat[k])
    if 'SASK' in k:
        sasdict.update(initDat[k])
        
dictL = [edmdict, caldict, vicdict, sasdict]
dictN = ["Edmonton", "Calgary", "Victoria", "Saskatoon"]

## Let's find a list of common dates where we have weather data for all cities. 
dtlists = [set(k for k,d in D.items() if len(d[ncl[0]])!=0 and len(d[ncl[1]])!=0 and len(d[ncl[2]])!=0) for D in dictL]

## intersection of all the sets
comdt = set.intersection(*dtlists)
## sort the dates.
coml = sorted(comdt)

## for all the cities, and all the common dates, 
## we convert all the measured termperature and precipitation
## items to floats. Here we add the (not too bad) assumption that if precipitation
## is not listed, it should be zero.

for D in dictL:
    for x in coml:
        for k in range(len(ncl)):
            if len(D[x][ncl[k]])==0:
                D[x][ncl[k]]=0.0
            else:
                D[x][ncl[k]]=float(D[x][ncl[k]])
           
with open("data/Victoria (BC) Police Department.geojson") as f:
    data = json.loads(f.read())
    
ctree = dict()

for R in data['features']:
    TopI = R['properties']['parent_incident_type']
    BotI = R['properties']['incident_type_primary']
    if TopI not in ctree.keys():
        ctree[TopI] = co.defaultdict(int)
    ctree[TopI][BotI] += 1
    
clean_dat = list()
incompl_dat = list()

for x in data['features']:
    if 'properties' not in x.keys():
        continue ## why bother?

    ## we have the properties, so let's start building the record.
    newRec = dict()
    incFlag = False # set to true if we discover missing data in x
    
    floatkeys = ['latitude', 'longitude']
    strkeys = ['parent_incident_type', 'incident_type_primary', 'address_1', 'address_2']
    intkeys = ['case_number', 'incident_id']
    datekeys = ['created_at', 'updated_at', 'incident_datetime']
    
    for k in floatkeys:
        if k in x['properties'].keys() and isinstance(x['properties'][k], str) and\
        len(x['properties'][k])>0:
            newRec[k] = float(x['properties'][k])
        else:
            incFlag=True

    ## anything to check?
    for k in strkeys:
        newRec[k] = x['properties'][k]
        
    for k in intkeys:
        ## let's count non-numerical characters
        non_ch_chars = []
        digits = '0123456789'
        for ch in x['properties'][k]:
            if ch not in digits:
                non_ch_chars.append(ch)

        for ch in non_ch_chars:
            if ch != '-':
                x['properties'][k] = x['properties'][k].replace(ch, '-')
            
        if '-' in x['properties'][k]:
            newRec[k] = [int(w) for w in x['properties'][k].split('-')]
        else:
            newRec[k] = int(x['properties'][k])
            
    for k in datekeys:
        ## typical format: '2014-12-06T21:59:00.000'
        newRec[k] = dt.datetime.strptime(x['properties'][k], '%Y-%m-%dT%H:%M:%S.000')
        
    if incFlag:
        incompl_dat.append(newRec)
    else:
        clean_dat.append(newRec)
        
## Let's use the results from the lab earlier this week to fix or purge the clearly bad data from
## clean_dat...

bad_idx = []

for i in range(len(clean_dat)):
    x = clean_dat[i]
    if x['latitude']>48.655 or x['latitude']<48:
        bad_idx.append(i)
        continue
    if x['longitude']<-124 or x['longitude']>-123:
        bad_idx.append(i)
        continue
    if x['incident_datetime'] > x['created_at']:
        bad_idx.append(i)
        continue
    if x['updated_at'] < x['created_at']:
        bad_idx.append(i)
        
clean_dat = [clean_dat[i] for i in range(len(clean_dat)) if i not in bad_idx]

