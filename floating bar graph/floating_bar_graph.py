# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:31:04 2018
Plotting AOI over time from Pro Lab data export
@author: Richard Andersson @ Tobii Pro

Requires the Python package Matplotlib
(Ought to be part of any decent scientific Python installation)

Plots by fixation and not visits/dwells.
Handles overlapping AOIs.

Limitations:
Only for one participant and not many. (the fixation times will overlap and 
just create long streaks for the AOIs and not the transition patterns we want)

No warranties or guarantees!

"""



# POINT FILENAME TO YOUR EXPORTED DATA FILE HERE
filename = r'Data Export.tsv' # Add path as needed.
###############################################################################

# EXTRACT FIXATIONS AND AOI HITS FROM FILE
import re

start_list = []
dur_list = []
name_list = []

# Change encoding to 'utf-8-sig' for Pro Lab versions before 1.138
with open(filename, mode='r', encoding='utf-8') as x:
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
    
    if len(aoicolnames) < 1:
        raise Exception('No AOI columns part of data file!')
    
except:
    print("Being able to locate the correct columns is a requirement!")
    raise


# SETTING TIME START
start_time = None
for i in range(1,len(dat)):
    elems = dat[i].strip().split('\t')
    if start_time is None and elems[ti] != '':
        start_time = int(elems[ti])
        break


# PROCESS FIXATION DATA
# for every aoi column (we process separately b/c not necessarily mutually exclusive)
for k in range(len(aoii)):
    current_em = None
    previous_em = None
    
    for i in range(1,len(dat)):
        elems = dat[i].strip().split('\t')
        
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
                    start_list.append( (int(elems[ti]) - start_time)/1000 )
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
plt.xlabel('Time (ms from start)')
plt.ylabel('Areas of interest')
plt.show()
