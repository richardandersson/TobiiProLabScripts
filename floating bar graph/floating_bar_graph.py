# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:31:04 2018
Plotting AOI over time from Lab data export
@author: Richard Andersson @ Tobii Pro

Requires the Python package Matplotlib
(Ought to be part of any decent scientific Python installation)

Plots fixations and not visits/dwells.
Handles overlapping AOIs.

No warranties or guarantees!

"""



# POINT FILENAME TO YOUR EXPORTED DATA FILE HERE
filename = r'data export.tsv' # Add path as needed.
###############################################################################

# EXTRACT FIXATIONS AND AOI HITS FROM FILE
import re

start_list = []
dur_list = []
name_list = []


with open(filename, mode='r', encoding='UTF-8-sig') as x:
    dat = x.readlines()


# Process header line and set up meta-information
elems = dat[0].strip().split('\t')
try:
    ti = elems.index('Recording timestamp') # timestamp column index
    emi = elems.index('Eye movement type index')
    eti = elems.index('Eye movement type')
    di = elems.index('Gaze event duration')
    
    aoii = [] # aoi column indices
    for j in range(len(elems)):
        if re.match('AOI hit', elems[j]):
            aoii.append(j)
    
    aoicolnames = [] # will store names given to the AOIs in Lab
    for j in range(len(aoii)):
        aoicolnames.append( re.findall('AOI hit \[.+ - (.+)\]', elems[aoii[j]])[0] )
    
except:
    print("Being able to locate the correct columns is a requirement!")
    raise
    




# for every aoi column (we process separately b/c not necessarily mutually exclusive)
for k in range(len(aoii)):
    current_em = None
    previous_em = None
    start_time = None
    
    for i in range(1,len(dat)):
        elems = dat[i].strip().split('\t')
        
        # If we have no start time of this recording yet, set this first
        if start_time is None and elems[ti] != '':
            start_time = elems[ti]

        if elems[eti] == 'Fixation' and elems[ti] != '':
            
            current_em = elems[emi] # update eye movement index
            
            if current_em == previous_em: # same eye movement event number as before, go to next data line
                continue
                
            else:
                try:
                    hit = elems[aoii[k]]
                except IndexError:
                    # Catches a case were there is a fixation, but no hit values in column (eye-tracker time when media end)
                    continue
                
                if hit == '1': # a new fixation and is an AOI-hit
                    start_list.append( int(elems[ti]) - int(start_time) )
                    dur_list.append( float(elems[di]) )
                    name_list.append( float(k) )
                    previous_em = current_em
                else:
                    continue
            
        else:
            pass # ignore lines due to, e.g., stimulus onset events


# PLOTTING THE DATA

import matplotlib.pyplot as plt

plt.barh(y=name_list, 
         width=dur_list, 
         left=start_list, 
         height=0.3)

ax = plt.gca()
ax.set_yticks(list(range(len(aoii))))
ax.set_yticklabels(aoicolnames)
plt.xlabel('Recording time')
plt.ylabel('Areas of interest')

