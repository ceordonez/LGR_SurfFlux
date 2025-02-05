#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
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

    temp = cfg["Air"]["Temp"]
    press = cfg["Air"]["Pres"]
    vol = cfg["Chamber"]["Volume"]
    area = cfg["Chamber"]["Area"]
    var = cfg["variable"]

    temp_k = temp + 273.15
    m = 8.31451 * temp_k / (press * 100) * 1000  # Molar Volume (L/mol)
    itime = data.index.values
    time = data.index.to_pydatetime().tolist()

    # Selecting variables to process
    if var == "CH4":
        var = "[CH4]d_ppm"
    elif var == "CO2":
        var = "[CO2]d_ppm"
    # cdata = data[var]
    # Create matrix to save the results
    # Add results to matrix
    p1 = []
    idxs1 = []
    idxs2 = []
    tstart = []
    tend = []
    vstart = []
    vend = []
    slopes = []
    vres = []
    pearson = []
    fluxes = []
    fids = []

    for pt in range(len(pts[0][::2])):

        idx1 = int(abs((itime - pts[0][2 * pt])).argmin())
        idx2 = int(abs((itime - pts[0][2 * pt + 1])).argmin())

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            range(len(time[idx1 : idx2 + 1])), data[var][idx1 : idx2 + 1]
        )
        p1.append(intercept)
        idxs1.append(idx1)
        idxs2.append(idx2)
        tstart.append(pd.to_datetime(time[idx1]))
        tend.append(pd.to_datetime(time[idx2]))
        vstart.append(data.iloc[idx1][var])
        vend.append(data.iloc[idx2][var])
        slopes.append(slope)
        vres.append(std_err)
        pearson.append(r_value)
        fluxes.append(slope * vol / (m * area) * 86.4)
        fids.append(pt + 1)

    data = {
        "FID": fids,
        "ID start": idxs1,
        "ID end": idxs2,
        "Time start": tstart,
        "Time end": tend,
        "Value start (ppm)": vstart,
        "Value end (ppm)": vend,
        "Slope (ppm/s)": slopes,
        "Std Error": vres,
        "Pearson": pearson,
        "Flux (mmol/m2/d)": fluxes,
        "Temp (degC)": temp,
        "Press (hPa)": press,
    }
    points = pd.DataFrame(
        data,
        index=range(len(pts[0][::2])),
    )
    return points, p1
