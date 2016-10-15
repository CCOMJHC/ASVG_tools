#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 12:11:15 2016

@author: Val Schmidt
Center for Coastal and Ocean Mapping
University of New Hampshire
Copyright 2016
All rights reserved.

asvlog is a python class and module for parsing, manipulating and plotting logs 
from ASV Global, C-Worker 4 logs. 
"""

import os
import pandas
import scipy.io as sio
import math

class asvlog(object):
    '''
    An asvlog is an ASV log file type, exported into CSV format.
    '''
    
    LOG_ID = { \
        'engine' :  1, \
        'payload':  2, \
        'vehicle':  3, \
        'pilot'  :  4, \
        'vehicle_processor' : 5, \
        'vehicle_state'     : 6, \
        'vs_remote_control' : 7 }
    
    data = "";
        
    def __init__(self, filename):
        '''
        Initializes the class with a string to the data file.
        '''

        self.filename = os.path.basename(filename)
        self.pathname = os.path.dirname(filename)
        self.pathandfile = filename
        
        self.debug = False
        self.verbosity = 0
        self.id = None    
        self.log_version = 0.1
        pass
    
    def identify(self):
        '''
        A function to identify the log type and version.
        '''
    
        # Log version is not used yet.
        self.log_version = 0.1

        # FIX: Does this make any sense? Can we just use the log name? 
        # Eventually one could read the first line of the log to identify it if the     
        LOG_ID = { 
            'engine' :  1, 
            'payload':  2, 
            'vehicle':  3, 
            'pilot'  :  4, 
            'vehicle_processor' : 5, 
            'vehicle_state'     : 6, 
            'vs_remote_control' : 7 }
            
        self.logtype = LOG_ID.get(self.filename[:-4])
    
    def parse(self):
        '''
        Use pandas data parsing routines to parse CSV data into pandas DataFrame. 
        
        The unix epoch time is set as the DataFrame Index. 
        The headers in the file are used to label the columns.
        
        To get a list of fields use data.columns
        '''
        
        # self.data = pandas.read_csv(self.pathandfile,header=0,index_col=0)
        self.data = pandas.read_csv(self.pathandfile,header=0)
        # self.data.index = pandas.to_datetime((self.data.index.values),unit='s')
        self.data.index = pandas.to_datetime((self.data['Epoch Time (s)']),unit='s')
        self.fields = self.data.columns  
        
    def plot(self):
        '''
        A method to quickly plot all the fields
        '''
        
        # Calculate the number of subplots. 
        maxplotrows = 4
        rows, fields = self.data.shape()
        maxplotcols = math.floor(fields/maxplotrows)
        if fields > maxplotrows and fields % maxplotrows > 0:
            maxplotcols = maxplotcols + 1
            
        # Plot the data. 
        H = self.data.plot.line(layout=(4,3),
                                subplots=True,
                                style={'color':'black','linewidth':3} # Doesn't work!
                                )
        return H
        
    def save_to_mat(self,matfilename = '',verbosity = 0):
        '''
        Method to save to MATLAB format
        '''
      
        # A tricky way to convert the DataFrame to a dictionary.
        # See: http://stackoverflow.com/questions/30669137/python-pandas-dataframe-to-matlab-struct-using-scipy-io
        a_dict = {col_name : self.data[col_name].values \
            for col_name in self.data.columns.values}

        if verbosity > 2:
            print "Converting field names to MATLAAB compatible ones."                
            
        # Modify the keys to MATLAB compatiable variable names. (35 characters max)            
        for key in a_dict.keys():
            oldkey = key
            key = key.rstrip()
            key = key.replace('Speed Control','SpeedCtl')
            key = key.replace('Throttle Control','SpeedCtl')   
            key = key.replace('Course Control','CourseCtl')
            key = key.replace('Heading Control','HeadingCtl')
            key = key.replace('Steering Control','SteeringCtl')
            key = key.replace('Drive Train','DrvTrn')
            key = key.replace('Proportional','Kp')
            key = key.replace('Derivative','Kd')
            key = key.replace('Integral','Ki')
            key = key.replace('Commanded','Cmded')
            key = key.replace('Position','Pos')
            key = key.replace('Measured','Meas')
            key = key.replace('Engine','Eng')
            key = key.replace('Desired','Des')
            key = key.replace('Effort','Eff')
            key = key.replace('Temperature','Temp')
            key = key.replace('Control','Ctrl')
            key = key.replace(' (','_')
            key = key.replace(' | ','_')
            key = key.replace(' ','_')
            key = key.replace('(','_')
            key = key.replace(')','')
            key = key.replace('%','Pct')
            
            key = key.replace('|','_')
            if key.startswith('1'):
                key = 'One' + key[1:]

            if verbosity > 2:            
                print "\tOriginal Field: " + oldkey + "\t\tNew Field:" + key + ' (' + str(key.__len__()) + ')'
            a_dict[key] = a_dict.pop(oldkey)

        # This step creates a structure having the file name with fields for each key in a_dict.
        tmp = {self.filename[:-4]: a_dict}
        # Create a default file name.
        if matfilename == '':
            matfilename = self.filename[:-3] + 'mat'
        
        # Write the file.
        sio.savemat(os.path.expanduser(matfilename),tmp)
            
