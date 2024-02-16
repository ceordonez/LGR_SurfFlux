#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from scipy import stats

from src.plots import plot_select_points

def processing_data(data, cfg):
    """Process data.

    Parameters
    ----------
    data: DataFrame
        LGR data
    cfg: dictionary
        Configuration information

    Returns
    -------
    TODO
    """
    pts_sel = plot_select_points(data, cfg)

    results, p1 = calculate_fluxes(cfg, data, pts_sel)

    return results, p1


def calculate_fluxes(cfg, data, pts):

    temp = cfg['Air']['Temp']
    press = cfg['Air']['Pres']
    vol = cfg['Chamber']['Volume']
    area = cfg['Chamber']['Area']
    var = cfg['variable']

    temp_k = temp + 273.15
    m = 8.31451*temp_k/(press*100)*1000 #Molar Volume (L/mol)
    itime = data.index.values
    time = data.index.to_pydatetime().tolist()

    # Selecting variables to process
    if var == 'CH4':
        var='[CH4]d_ppm'
    elif var == 'CO2':
        var = '[CO2]d_ppm'
    #cdata = data[var]
    # Create matrix to save the results
    points = pd.DataFrame(index=range(len(pts[0][::2])),
                        columns=['FID','ID start', 'ID end', 'Time start', 'Time end',
                                'Value start (ppm)', 'Value end (ppm)', 'Slope (ppm/s)',
                                'Res', 'R2','Flux (mmol/m2/d)','Temp','Press'])
    # Add results to matrix
    points['Temp'][0] = temp
    points['Press'][0] = press
    p1 = []

    for pt in range(len(pts[0][::2])):
        idx1 = abs((itime-pts[0][2*pt])).argmin()
        idx2 = abs((itime-pts[0][2*pt+1])).argmin()
        points['ID start'][pt] = idx1
        points['ID end'][pt] = idx2
        points['Time start'][pt] = time[idx1]
        points['Time end'][pt] = time[idx2]
        points['Value start (ppm)'][pt] = data.iloc[idx1][var]
        points['Value end (ppm)'][pt] = data.iloc[idx2][var]

        idx1 = points['ID start'][pt]
        idx2 = points['ID end'][pt]

        # Calculation linea interpolation and fluxes
        pol,res, _, _, _ = np.polyfit(range(len(time[idx1:idx2+1])),
                                    data[var][idx1:idx2+1], 1, full=True)
        p = np.poly1d(pol)
        slope, intercept, r_value, p_value, std_err = \
            stats.linregress(range(len(time[idx1:idx2+1])),
                                data[var][idx1:idx2+1])
        p1.append(pol[1])
        points['Slope (ppm/s)'][pt] = pol[0]
        points['Res'][pt] = res[0]
        points['R2'][pt] = r_value**2
        points['Flux (mmol/m2/d)'][pt] = pol[0]*vol/(m*area)*86.4
        points['FID'][pt] = pt + 1

    return points, p1
