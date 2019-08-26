# -*- coding: utf-8 -*-
"""
Created on 2019-04-04
Computing AOI transition matrix from Tobii Pro Lab Data Export file.
@author: Richard Andersson @ Tobii Pro

Requires the Python package Matplotlib and Numpy
(Ought to be part of any decent scientific Python installation)

Shows transition matrix for a data export.
If you use a data file from several recordings, you will get data aggregated across
those recordings.
Ignores whitespace transitions, i.e. from a non-AOI to an AOI or vice-versa.
AOI2 -> whitespace -> AOI1 -> AOI2 -> whitespace (only one transition, from AOI1 to AOI2)
Fixations inside an AOI are also counted, but are easy to disregard.

No warranties or guarantees!
"""



# POINT FILENAME TO YOUR EXPORTED DATA FILE HERE
filename = r'transition test Data Export.tsv' # add path if needed
###############################################################################

# EXTRACT FIXATIONS AND AOI HITS FROM FILE
import re
import numpy as np


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
    raise Exception("Being able to locate the correct columns is a requirement!")


transmatrix = np.zeros(shape=(len(aoii), len(aoii)), dtype='uint32')

current_em = None
previous_em = None
start_time = None
current_aoi = None
previous_aoi = None

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
            temp_hit_list = []
            # Go through all AOI columns immediately to catch signs of overlapping AOIs.
            for k in range(len(aoii)):
                try:
                    if elems[aoii[k]] == '1':
                        temp_hit_list.append(1)
                    else:
                        temp_hit_list.append(0)
                except IndexError:
                # Catches a case were there is a fixation, but no hit (empty) values in column (when media end)
                    continue
            
            if sum(temp_hit_list) > 1:
                raise Exception("Overlapping AOIs are not allowed! Not possible to calculate transitions.")
            elif sum(temp_hit_list) == 1:
                current_aoi = temp_hit_list.index(1)
            else:
                current_aoi = None
                
            if previous_aoi is not None and current_aoi is not None:
                transmatrix[previous_aoi, current_aoi] += 1
#                print("From {0} To {1}".format(previous_aoi, current_aoi))
            
            previous_aoi = current_aoi
            current_aoi = None
            previous_em = current_em
            
    else:
        pass # ignore lines due to, e.g., stimulus onset events


# PLOTTING THE DATA
print(transmatrix)
import matplotlib.pyplot as plt
plt.imshow(transmatrix, cmap='inferno')
ax = plt.gca()
ax.set_xticks(list(range(len(aoii))))
ax.set_xticklabels(aoicolnames)
ax.set_yticks(list(range(len(aoii))))
ax.set_yticklabels(aoicolnames)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 
plt.colorbar()
for i in range(len(transmatrix)):
    for j in range(len(transmatrix)):
        ax.annotate(str(transmatrix[i,j]),xy=(j,i),bbox=dict(facecolor='white', edgecolor='white', alpha=0.5))
plt.ylabel('From AOI')
plt.xlabel('To AOI')

plt.show()
