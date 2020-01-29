#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy import stats
from matplotlib.dates import date2num

def processing_data(pts, rfile, n, Temp, Press, Vol, Area, var):

    Tk = Temp + 273.15
    M = 8.31451*Tk/(Press*100)*1000 #Molar Volume (L/mol)
    time = rfile.index.values

    # Selecting variables to process
    if var == 'CH4':
        nvar = 0
    elif var == 'CO2':
        nvar = 1
    cdata = rfile.keys()[nvar]

    # Create matrix to save the results
    points = pd.DataFrame(index=range(n),
                        columns=['FID','ID start', 'ID end', 'Time start', 'Time end',
                                'Value start (ppm)', 'Value end (ppm)', 'Slope (ppm/s)',
                                'Res', 'R2','Flux (mmol/m2/d)','Temp','Press'])
    # Add results to matrix
    points['Temp'][0] = Temp
    points['Press'][0] = Press
    p1 = []
    for pt in range(n):
        idx1 = abs((date2num(time)-pts[2*pt][0])).argmin()
        idx2 = abs((date2num(time)-pts[2*pt+1][0])).argmin()
        points['ID start'][pt] = idx1
        points['ID end'][pt] = idx2
        points['Time start'][pt] = time[idx1]
        points['Time end'][pt] = time[idx2]
        points['Value start (ppm)'][pt] = rfile[cdata][idx1]
        points['Value end (ppm)'][pt] = rfile[cdata][idx2]

        idx1 = points['ID start'][pt]
        idx2 = points['ID end'][pt]

        # Calculation linea interpolation and fluxes
        pol,res, _, _, _ = np.polyfit(range(len(time[idx1:idx2+1])),
                                    rfile[cdata][idx1:idx2+1], 1, full=True)
        p = np.poly1d(pol)
        slope, intercept, r_value, p_value, std_err = \
            stats.linregress(range(len(time[idx1:idx2+1])),
                                rfile[cdata][idx1:idx2+1])
        p1.append(pol[1])
        points['Slope (ppm/s)'][pt] = pol[0]
        points['Res'][pt] = res[0]
        points['R2'][pt] = r_value**2
        points['Flux (mmol/m2/d)'][pt] = pol[0]*Vol/(M*Area)*86.4
        points['FID'][pt] = pt + 1
    return points, p1, cdata
