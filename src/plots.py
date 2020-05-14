#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pdb
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import date2num, num2date
import numpy as np

from matplotlib.widgets import Cursor
from pandas.plotting import register_matplotlib_converters
from decimal import Decimal
register_matplotlib_converters()
mpl.use('tkAgg')

line = []
sc = []
pts = []
xydata_b = []

def plot_select_points(rfile, var):

    cdata1 = rfile.keys()[0]
    cdata2 = rfile.keys()[1]
    pts = []
    # Creating plot to select points per flux
    #fig = plt.figure(figsize=(25, 10))
    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(111, facecolor='#FFFFCC')
    ax2 = ax1.twinx()
    ax2.yaxis.tick_left()
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax2.yaxis.set_label_position("left")
    global line
    global sc
    if var == 'CO2':
        ax1.plot(rfile[cdata1], 'b', linewidth=3)
        line = ax2.plot(rfile[cdata2], 'k', linewidth=3, picker=5)[0]
        ax1.set_ylabel('CH4 (ppm)')
        ax2.set_ylabel('CO2 (ppm)')
        ax1.yaxis.label.set_color('b')
        ax1.spines['left'].set_color('b')
        ax1.tick_params(axis='y', which='both', colors='b')
        xdata = rfile.index.values
        ydata = [None, None]
        #sc = ax2.plot(rfile[cdata2], 'or', picker=5, alpha=1)
        sc = ax2.plot(xdata[0:2], ydata, 'or', picker=10)[0]
    if var == 'CH4':
        line = ax2.plot(rfile[cdata1], 'b', linewidth=3, picker=5)[0]
        ax1.plot(rfile[cdata2], 'k', linewidth=3)
        ax2.set_ylabel('CH4 (ppm)')
        ax1.set_ylabel('CO2 (ppm)')
        ax2.yaxis.label.set_color('b')
        ax2.spines['left'].set_color('b')
        ax2.tick_params(axis='y', which='both', colors='b')
        xdata = rfile.index.values
        ydata = [None, None]
        sc = ax2.plot(xdata[0:2], ydata, 'or', picker=10)[0]

    def add_or_remove_point(event):
        global line
        xydata_a = line.get_data()
        xdata_a = line.get_xdata()
        ydata_a = line.get_ydata()
        global sc
        xdata_b = sc.get_xdata()#sc.get_offsets()[:,0]
        ydata_b = sc.get_ydata() #sc.get_offsets()[:,1]
        global xydata_b
        xydata_b = [xdata_b[2:], ydata_b[2:]]
        #click x-value
        xdata_click = event.xdata
        #index of nearest x-value in a
        xdata_nearest_index_a = (np.abs(date2num(xdata_a)-xdata_click)).argmin()
        #new scatter point x-value
        new_xdata_point_b = date2num(xdata_a[xdata_nearest_index_a])
        #new scatter point [x-value, y-value]
        new_xdata_b = [xydata_a[0][xdata_nearest_index_a]]
        new_ydata_b = [xydata_a[1][xdata_nearest_index_a]]
        if event.button == 1:
            if new_xdata_point_b not in xdata_b:
                #insert new scatter point into b
                new_xdata_b = np.append(xdata_b, new_xdata_b)
                new_ydata_b = np.append(ydata_b, new_ydata_b)
                new_xydata_b = [new_xdata_b, new_ydata_b]
                #update sc
                sc.set_data(new_xydata_b)
                plt.draw()
        elif event.button == 3:
            #remove xdata point b
            if new_xdata_b:
                new_xdata_b = xdata_b[:-1]
                new_ydata_b = ydata_b[:-1]
                new_xydata_b = [new_xdata_b, new_ydata_b]
                #update sc
                sc.set_data(new_xydata_b)
                plt.draw()
        elif event.button == 2:
            plt.close()

    cursor = Cursor(ax=ax2, useblit=True, color='red', linewidth=2)
    fig.canvas.mpl_connect('button_press_event',add_or_remove_point)
    plt.show()
    return xydata_b

def plot_perflux(rfile, results, p1, cdata, path_out, lake, txtfile, date, var):

    ## Making forlder outs if does not exist
    path_results = os.path.join(path_out,lake,'Results','LGR')
    path_figout = os.path.join(path_results,'Figures_'+date)

    if not os.path.exists(path_results):
        os.makedirs(path_results)
    if not os.path.exists(path_figout):
        os.makedirs(path_figout)
    time = rfile.index.values
    for pt in range(len(results)):
        # Creation figures per flux
        idx1 = results['ID start'][pt]
        idx2 = results['ID end'][pt]
        r_value = results['R2'][pt]
        pol0 = results['Slope (ppm/s)'][pt]
        pol1 = p1[pt]
        p = np.poly1d([pol0, pol1])
        figf = plt.figure(figsize=(7,5))
        axf = figf.add_subplot(111)
        cR2 = u'R$^2$ = %0.2f' % (r_value**2)
        cf = u'$f(x)$ = %0.2E$x$ + %0.2f' % (Decimal(pol0),pol1)
        text = cf +'\n'+cR2
        axf.plot(range(len(time[idx1:idx2+1])),rfile[cdata][idx1:idx2+1],'o',
                label='LRG data')
        axf.plot(range(len(time[idx1:idx2+1])),
                p(range(len(time[idx1:idx2+1]))),'k-',label=text)
        plt.legend()
        axf.set_xlabel('Time (second)')
        axf.set_ylabel(cdata.strip())
        figffile = var + '_' + lake + '_Flux_' + str(pt + 1) + '_' +  txtfile + '.png'
        figf.savefig(os.path.join(path_figout,figffile), format = 'png', dpi=300)
        plt.close(figf)
    plt.close()

def plot_alldata(rfile, points, path_out, lake, var, txtfile, date, cdata):

    path_results = os.path.join(path_out,lake,'Results','LGR')
    path_figout = os.path.join(path_results,'Figures_'+date)

    if not os.path.exists(path_results):
        os.makedirs(path_results)
    if not os.path.exists(path_figout):
        os.makedirs(path_figout)
    time = rfile.index.values

    # Creating figure of the entire dataset of LGR file
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    ax.plot(time,rfile[cdata],linewidth=3, label='LGR data')
    ax.plot(points['Time start'], points['Value start (ppm)'],'ko',label='Selected points')
    ax.plot(points['Time end'], points['Value end (ppm)'],'ko')
    ax.set_xlabel('Time')
    ax.set_ylabel(cdata)
    plt.legend()
    figfilename = lake + '_points_' + var + '_' + txtfile+'.png'
    fig.savefig(os.path.join(path_figout, figfilename), format = 'png', dpi=300)
    plt.close()
