#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pandas as pd
import yaml


def footer_pos(filename):
    """Find footer position in LGR file.

    Parameters
    ----------
    filename: String
        File name of LGR file

    Returns
    -------
    ifooter: Int
        Starting line numnber of the footer of LGR file
    """
    with open(filename) as z:
        i = 0
        foot = False
        for line in z:
            if line.startswith("-----B"):
                ib = i
                foot = True
            i += 1
        if foot:
            ifooter = i - ib
        else:
            ifooter = 0
    return ifooter


def read_data(cfg):
    """Read LGR file.

    Parameters
    ----------
    cfg: dictionary
        Configuration information

    Returns
    -------
    data: DataFrame
        Data in lgr_file
    """
    # filename = os.path.join(path, lake, 'Data', 'LGR', date, txtfile+'.txt')
    date = cfg["date"]
    path = cfg["path_in"]
    inputfile = cfg["file"]

    filename = os.path.join(path, date, inputfile + ".txt")
    ifoot = footer_pos(filename)

    ## Reading column 0 is time, column 7 [CH4]d_ppm and column 9 [CO2]d_ppm
    data = pd.read_csv(
        filename,
        sep=",",
        header=1,
        skipfooter=ifoot,
        parse_dates=[0],
        usecols=[0, 7, 9],
        engine="python",
    )
    data = data.iloc[3:]  # get rid off the data when LGR is turn on
    cols = data.columns.values
    data.columns = [item.strip() for item in cols]
    data.Time = data.Time.dt.floor("s")
    data.set_index("Time", inplace=True)
    return data


def read_config(filename):
    """Read configuration file.

    Parameters
    ----------
    filename : string
        File name of the configuration process file

    Returns
    -------
    conf_file: dictionary
        Configuration data

    """
    with open(filename, "r") as file:
        conf_file = yaml.safe_load(file)
    return conf_file
