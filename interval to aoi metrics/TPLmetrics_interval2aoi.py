# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 21:03:38 2020

You have an interval-based metrics export from Tobii Pro Lab, but you would 
prefer it in the longer format, with one row per AOI per interval? No problem!

Script assumes you don't use periods as part of AOI or AOI tag names, because 
periods will be used to identify the start of the AOI name/tag.

Also excludes metrics with "Events" in the name, because otherwise events may 
be misidentified as an AOI.

Script will try to drop metrics that do not belong to any AOI (i.e. general 
interval/non-AOI metrics), because they become very confusable with AOI metrics 
since there will be a column specifying AOI for every row.

Will resave your specific file with the suffix "- LONG".


META1    METRIC1.AOI    METRIC2.AOI
jane         5               10

...becomes...

META1    METRIC    AOI
jane    metric1    5
jane    metric2   10


@author: Richard Andersson, Tobii Pro

Written/tested with Python 3.7.
Requires the package Pandas.
Tested with metrics from Tobii Pro Lab 1.130
"""

import pandas as pd
import re


def TPLmetrics_interval2aoi(filename):

    df = pd.read_csv(filename, sep='\t', header=0)
    
    meta_columns = []
    AOI_columns = []
    AOI_values = []
    nonAOImetrics_columns = [] # Non-AOI metrics: will be dropped
    
    for i in df.columns:
    
        if len(re.findall('\w\.\w+$', i)) != 0: # if metric succeeded by AOI name/tag
            
            if len(re.findall('\w+Events?\..+$', i)) != 0: # if event metric
                meta_columns.append(i)
                continue
            
            else: # AOI metric
                AOI_columns.append(i) # appends full name of metrics column
                AOI_values.append(re.findall('\.(\w+)$',i)[0]) # appends just AOI/AOItag name
            
        else: # not followed by AOI name/tag
            
            if len(re.findall('[_ ]fixations?$|[_ ]saccades?$', i)) != 0: # if it is a non-AOI metric - store name so we can drop it.
                nonAOImetrics_columns.append(i)
                continue
            
            else:
                meta_columns.append(i)
                continue
    
    
    # drop non-AOI metrics
    df.drop(nonAOImetrics_columns, axis=1, inplace=True)
    
    # melt to long format
    df = df.melt(id_vars = meta_columns, var_name='MetricAOI', value_name='value')
    df[['Metric','AOI']] = df.MetricAOI.str.split(".",expand=True)
    
    # Then group back up again
    meta_columns.extend(['AOI', 'Metric'])
    df = df.groupby(meta_columns)['value'].aggregate('mean').unstack()
    df = df.reset_index()
    
    # Export to tsv file
    new_filename = re.findall('(.+)\.tsv', filename)[0] + ' - LONG.tsv'
    df.to_csv(new_filename, sep='\t')


if __name__ == '__main__':
    filename = r'my metrics export.tsv'
    TPLmetrics_interval2aoi(filename)