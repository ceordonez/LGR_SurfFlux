#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

def footer_pos(LGRfile):
    """find footer position
    """
    with open(LGRfile) as z:
        i = 0
        foot = False
        for line in z:
            if line.startswith('-----B'):
                ib = i
                foot = True
            i+=1
        if foot:
            ifooter = i - ib
        else:
            ifooter = 0
    return ifooter

def read_data(path, lake, date, txtfile):
    """Reading LGR file
    """
    filename = os.path.join(path, lake, 'Data', 'LGR', date, txtfile+'.txt')
    ifoot = footer_pos(filename)
    ## Reading column 0 is time, column 7 [CH4]d_ppm and column 9 [CO2]d_ppm
    rfile = pd.read_csv(filename, sep=',', header=1, skipfooter=ifoot, squeeze=True,
                        infer_datetime_format=True, parse_dates=[0],usecols=[0,7,9],
                        engine='python', index_col=[0])
    rfile = rfile.iloc[3:] # get rid off the data when LGR is turn on
    return rfile

