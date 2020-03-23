#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import pdb

from pandas.plotting import register_matplotlib_converters
from decimal import Decimal
register_matplotlib_converters()
mpl.use('tkAgg')


def plot_select_points(rfile, n):

    cdata1 = rfile.keys()[0]
    cdata2 = rfile.keys()[1]

    # Creating plot to select points per flux
    fig,ax1 = plt.subplots(1,1,figsize=(25,10))
    ax2=ax1.twinx()
    ax1.plot(rfile[cdata1],'b',linewidth=3)
    ax2.plot(rfile[cdata2],'k',linewidth=3)
    #ax1.set_ylim(1,10)
    ax1.set_ylabel('CH4 (ppm)')
    ax2.set_ylabel('CO2 (ppm)')
    ax1.yaxis.label.set_color('b')
#    ax2.yaxis.label.set_color('r')
    ax1.spines['left'].set_color('b')
#    ax2.spines['right'].set_color('r')
    ax2.spines['left'].set_visible(False)
    ax1.tick_params(axis='y', which='both',colors='b')
#    ax2.tick_params(axis='y', which='both',colors='r')
    pts = plt.ginput(2*n,timeout=-1) # select points from plot
    return pts

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
