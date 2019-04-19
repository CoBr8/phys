# %% markdown
# ## Plotting lab
#
# For this plotting lab, we ask you to load the weather data for Edmonton, Calgary, Victoria and Saskatoon. Ensure you have found the set of dates where you have weather data for all four cities.
# %%
## This is the import code from 12.Matplotlib.
## You should be able to run it now, but perhaps you might have to modify the subdirectory
## list, sdp, depending on where you stored your weather files.

import datetime as dt
import os as os
from operator import itemgetter
import collections as co
import fnmatch as fn    ## library for finding files using OS wildcards
import numpy as np

print("Python current working directory:", os.getcwd())

## directories containing the weather w.* subdirectories
sdp = ['./L8.data', '../data']

## Build the list of directories of the weather files.
wsubdirs = sum( [[x+'/'+y for y in fn.filter(os.listdir(x), "w.*")] for x in sdp], [] )

print("Relative location of weather .csv files: ", wsubdirs)
# %%
## basic line formatting. This is used in the next code block.
## Code removes quotes and newlines, and splits along commas.
def fmtline(ln):
    PL = ln.translate({ord(c): None for c in '"\n'})
    PL = PL.split(",")
    return(PL)
# %%
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
# %%
## date gap check for initDat, i.e. report what (if any) days have missing weather data.
for A in initDat.keys():
    print("Airport: ", A, ' ', end='')
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
        print(sd[-1].date()-sd[0].date())

## list of keys we will have use for.
ncl = ['Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)', 'Total Precip (mm)']

## let's make sure all the max, min, mean, total rain, total snow, total precip floats are present
for A in initDat.keys():
    for k in ncl:
        am = 0
        for d in initDat[A].keys():
            if len(initDat[A][d][k])==0:
                am += 1
        print('Airport: ', A, 'missing ', k, ' count ', am)
# %%
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

# %%
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

# %% markdown
# **Exercise 1:**  For each year between 2014 and 2018 (i.e. where we have data for all the four cities), make a pie chart.  The slices of the pie fractions (or sizes) will be the percentage of days (for that year) where that city has the highest maximum temperature.  Ensure each slice is labelled by the city name.
# %%
import matplotlib.pyplot as plt
%matplotlib inline


# %% markdown
# **Exercise 2:** Repeat Exercise 1, but use only summer weather.
# %%
## Feel free to use June 21st as the first day of summer -- the actual date depends on the year, but
## given that we are making pie charts, being one day inaccurate is of little consequence.
## Similarly, use September 23rd for the start of Fall.


# %% markdown
# **Exercise 3:** Repeat Exercise 1, but use the number of days that city has the lowest maximum temperature (among the four cities).
# %%

# %% markdown
# **Exercise 4**: Repeat Exercise 3, but with summer weather.
# %%

# %% markdown
# **Exercise 5:** Repeat Exercise 1, using the percentage of days where a city has the most precipitation (among all four cities).
# %%

# %% markdown
# **Exercise 6:** Make a matplotlib plot where with two subplots.  The plot on the left will be from Exercise 2, and the plot on the right will be from Exercise 4.  i.e. the left pie chart will be the percentage of summer days with highest max temperature, the plot on the right will be the percentage of days with coldest max temperature.
# %%

# %%
