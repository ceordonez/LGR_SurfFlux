#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from decimal import Decimal

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from matplotlib.widgets import Cursor
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
mpl.use("tkAgg")

line = []
sc = []
pts = []
xydata_b = []


def plot_data(data, results, p1, cfg):
    """TODO: Docstring for plot_data.

    Parameters
    ----------
    data : TODO
    results : TODO
    p1 : TODO
    cfg : TODO

    Returns
    -------
    TODO

    """
    plot_perflux(data, results, p1, cfg)
    plot_alldata(data, results, cfg)


def plot_select_points(data, cfg):

    ylim_max = cfg["Plot"]["ylim_max"]
    ylim_min = cfg["Plot"]["ylim_min"]
    var = cfg["variable"]

    cdata1 = data.keys()[0]
    cdata2 = data.keys()[1]
    pts = []

    # Creating plot to select points per flux
    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(111, facecolor="#FFFFCC")
    ax2 = ax1.twinx()
    ax2.yaxis.tick_left()
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax2.yaxis.set_label_position("left")
    global line
    global sc
    if var == "CO2":
        ax1.plot(data[cdata1], "b", linewidth=3)
        line = ax2.plot(data[cdata2], "k", linewidth=3, picker=5)[0]
        ax1.set_ylabel("CH4 (ppm)")
        ax2.set_ylabel("CO2 (ppm)")
        ax1.yaxis.label.set_color("b")
        ax1.spines["left"].set_color("b")
        ax1.tick_params(axis="y", which="both", colors="b")
        xdata = data.index.values
        ydata = [None, None]
        # sc = ax2.plot(data[cdata2], 'or', picker=5, alpha=1)
        sc = ax2.plot(xdata[0:2], ydata, "or", picker=10)[0]
        if None not in (ylim_max, ylim_min):
            ax2.set_ylim([ylim_min, ylim_max])
        elif ylim_min is None:
            ax2.set_ylim([None, ylim_max])
        elif ylim_max is None:
            ax2.set_ylim([ylim_min, None])

    if var == "CH4":
        line = ax2.plot(data[cdata1], "b", linewidth=3, picker=5)[0]
        ax1.plot(data[cdata2], "k", linewidth=3)
        ax2.set_ylabel("CH4 (ppm)")
        ax1.set_ylabel("CO2 (ppm)")
        ax2.yaxis.label.set_color("b")
        ax2.spines["left"].set_color("b")
        ax2.tick_params(axis="y", which="both", colors="b")
        xdata = data.index.values
        ydata = [None, None]
        sc = ax2.plot(xdata[0:2], ydata, "or", picker=10)[0]
        if None not in (ylim_max, ylim_min):
            ax2.set_ylim([ylim_min, ylim_max])
        elif ylim_min is None:
            ax2.set_ylim([None, ylim_max])
        elif ylim_max is None:
            ax2.set_ylim([ylim_min, None])

    def add_or_remove_point(event):
        global line
        xydata_a = line.get_data()
        xdata_a = line.get_xdata()
        ydata_a = line.get_ydata()
        global sc
        xdata_b = sc.get_xdata()  # sc.get_offsets()[:,0]
        ydata_b = sc.get_ydata()  # sc.get_offsets()[:,1]
        global xydata_b
        xydata_b = [xdata_b[2:], ydata_b[2:]]
        # click x-value
        xdata_click = event.xdata
        # index of nearest x-value in a
        xdata_nearest_index_a = (np.abs(date2num(xdata_a) - xdata_click)).argmin()
        # new scatter point x-value
        new_xdata_point_b = date2num(xdata_a[xdata_nearest_index_a])
        # new scatter point [x-value, y-value]
        new_xdata_b = [xydata_a[0][xdata_nearest_index_a]]
        new_ydata_b = [xydata_a[1][xdata_nearest_index_a]]
        if event.button == 1:
            if new_xdata_point_b not in xdata_b:
                # insert new scatter point into b
                new_xdata_b = np.append(xdata_b, new_xdata_b)
                new_ydata_b = np.append(ydata_b, new_ydata_b)
                new_xydata_b = [new_xdata_b, new_ydata_b]
                # update sc
                sc.set_data(new_xydata_b)
                plt.draw()
        elif event.button == 3:
            # remove xdata point b
            if new_xdata_b:
                new_xdata_b = xdata_b[:-1]
                new_ydata_b = ydata_b[:-1]
                new_xydata_b = [new_xdata_b, new_ydata_b]
                # update sc
                sc.set_data(new_xydata_b)
                plt.draw()
        elif event.button == 2:
            plt.close()

    cursor = Cursor(ax=ax2, useblit=True, color="red", linewidth=2)
    fig.canvas.mpl_connect("button_press_event", add_or_remove_point)
    plt.show()
    return xydata_b


def plot_perflux(data, results, p1, cfg):

    path_out = cfg["path_out"]
    site = cfg["site"]
    lgrfile = cfg["file"]
    date = cfg["date"]
    var = cfg["variable"]

    if var == "CH4":
        vard = "[CH4]d_ppm"
    elif var == "CO2":
        vard = "[CO2]d_ppm"

    ## Making forlder outs if does not exist
    path_results = os.path.join(path_out, site, "Results", "LGR")
    path_figout = os.path.join(path_results, "Figures_" + date)

    if not os.path.exists(path_results):
        os.makedirs(path_results)
    if not os.path.exists(path_figout):
        os.makedirs(path_figout)
    time = data.index.values
    for pt in range(len(results)):
        # Creation figures per flux
        idx1 = results["ID start"][pt]
        idx2 = results["ID end"][pt]
        r_value = results["Pearson"][pt]
        pol0 = results["Slope (ppm/s)"][pt]
        pol1 = p1[pt]
        p = np.poly1d([pol0, pol1])
        figf = plt.figure(figsize=(7, 5))
        axf = figf.add_subplot(111)
        cR2 = "r = %0.2f" % (r_value)
        cf = "$f(x)$ = %0.2E$x$ + %0.2f" % (Decimal(pol0), pol1)
        text = cf + "\n" + cR2
        axf.plot(
            range(len(time[idx1 : idx2 + 1])),
            data[vard][idx1 : idx2 + 1],
            "o",
            label="LRG data",
        )
        axf.plot(
            range(len(time[idx1 : idx2 + 1])),
            p(range(len(time[idx1 : idx2 + 1]))),
            "k-",
            label=text,
        )
        plt.legend()
        axf.set_xlabel("Time (second)")
        axf.set_ylabel(vard)
        figffile = var + "_" + site + "_Flux_" + str(pt + 1) + "_" + lgrfile + ".png"
        figf.savefig(os.path.join(path_figout, figffile), format="png", dpi=300)
        plt.close(figf)
    plt.close()


def plot_alldata(data, points, cfg):

    path_out = cfg["path_out"]
    site = cfg["site"]
    var = cfg["variable"]
    lgrfile = cfg["file"]
    date = cfg["date"]
    if var == "CH4":
        vard = "[CH4]d_ppm"
    elif var == "CO2":
        vard = "[CO2]d_ppm"

    path_results = os.path.join(path_out, site, "Results", "LGR")
    path_figout = os.path.join(path_results, "Figures_" + date)

    if not os.path.exists(path_results):
        os.makedirs(path_results)
    if not os.path.exists(path_figout):
        os.makedirs(path_figout)
    time = data.index.values

    # Creating figure of the entire dataset of LGR file
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(time, data[vard], linewidth=3, label="LGR data")
    ax.plot(
        points["Time start"], points["Value start (ppm)"], "ko", label="Selected points"
    )
    ax.plot(points["Time end"], points["Value end (ppm)"], "ko")
    ax.set_xlabel("Time")
    ax.set_ylabel(var)
    plt.legend()
    figfilename = "_".join([site, "points", var, lgrfile + ".png"])
    fig.savefig(os.path.join(path_figout, figfilename), format="png", dpi=300)
    plt.close()
