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
    rfile = pd.read_csv(filename, sep=',', header=1, skipfooter=ifoot, squeeze=True,
                        infer_datetime_format=True, parse_dates=[0],usecols=[0,7,9],
                        engine='python', index_col=[0])
    rfile = rfile.iloc[3:-155]
    return rfile

