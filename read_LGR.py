#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os
import pdb
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from scipy import stats
from decimal import Decimal

########Soppen'

path = '../../../Data/Fieldwork/MultiLakeSurvey/Lakes'

path_out = '/home/cesar/Documentos/PhD/Data/MultiLakeSurvey/Lakes'
lake = 'Baldegg'
date = '2019-08-18'
txtfile = 'gga_'+date+'_f0001'
n = 8        # Number of fluxes
Temp = 30    # Air Temperature (Degree C)
Press = 959  # Pressure (hPa)
Vol = 16.76  # Volumen chamber (L)
Area = 0.126 # Area Chamber (m2)
var = 'CO2'  # Variable to read (CH4 or CO2)

print(os.getcwd())
################################################################################

Tk = Temp + 273.15
M = 8.31451*Tk/(Press*100)*1000 #Molar Volume (L/mol)

#Reading LGR file
filename = os.path.join(path, lake, 'Data', 'LGR', date, txtfile+'.txt')

def footer_pos(LGRfile):
    # find footer position
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

ifoot = footer_pos(filename)
rfile = pd.read_csv(filename, sep=',', header=1, skipfooter=ifoot, squeeze=True,
                    infer_datetime_format=True, parse_dates=[0],usecols=[0,7,9],
                    engine='python', index_col=[0])
rfile = rfile.iloc[3:-155]
## Making forlder outs if does not exist
path_results = os.path.join(path_out,lake,'Results','LGR')
path_figout = os.path.join(path_results,'Figures_'+date)

if not os.path.exists(path_results):
    os.makedirs(path_results)
if not os.path.exists(path_figout):
    os.makedirs(path_figout)

# Selecting variable to process
if var == 'CH4':
    nvar = 1
elif var == 'CO2':
    nvar = 2

time = rfile.index.values
cdata1 = rfile.keys()[0]
cdata2 = rfile.keys()[1]
cdata = rfile.keys()[nvar-1]

# Creating plot to select points per flux
fig,ax1 = plt.subplots(1,1,figsize=(25,10))
ax2=ax1.twinx()
ax1.plot(rfile[cdata1],'b',linewidth=3)
ax2.plot(rfile[cdata2],'r',linewidth=3)
#ax1.set_ylim(1,10)
ax1.set_ylabel('CH4 (ppm)')
ax2.set_ylabel('CO2 (ppm)')
ax1.yaxis.label.set_color('b')
ax2.yaxis.label.set_color('r')
ax1.spines['left'].set_color('b')
ax2.spines['right'].set_color('r')
ax2.spines['left'].set_visible(False)
ax1.tick_params(axis='y', which='both',colors='b')
ax2.tick_params(axis='y', which='both',colors='r')
pts = plt.ginput(2*n,timeout=-1) # select points from plot

# Create matrix to save the results
points = pd.DataFrame(index=range(2*n),
                      columns=['FID','ID start', 'ID end', 'Time start', 'Time end',
                               'Value start (ppm)', 'Value end (ppm)', 'Slope (ppm/s)',
                               'Res', 'R2','Flux (mmol/m2/d)','Temp','Press'])
# Add results to matrix
points['Temp'][0] = Temp
points['Press'][0] = Press
for pt in range(n):
    idx1 = abs((date2num(time)-pts[2*pt][0])).argmin()
    idx2 = abs((date2num(time)-pts[2*pt+1][0])).argmin()
    points['ID start'][pt] = idx1
    points['ID end'][pt] = idx2
    points['Time start'][pt] = time[idx1]
    points['Time end'][pt] = time[idx2]
    points['Value start (ppm)'][pt] = rfile[cdata][idx1]
    points['Value end (ppm)'][pt] = rfile[cdata][idx2]

# Cration of excel file and perform final calculations
excel_filename = var + '_' + lake + '_LGR_' + txtfile + '.xlsx'
excelpath = os.path.join(path_results, excel_filename)
writer = pd.ExcelWriter(excelpath, datetime_format='mmm d yyyy hh:mm:ss',
                        engine='xlsxwriter')
for pt in range(n):
    idx1 = points['ID start'][pt]
    idx2 = points['ID end'][pt]

    # Calculation linea interpolation and fluxes
    pol,res, _, _, _ = np.polyfit(range(len(time[idx1:idx2+1])),
                                  rfile[cdata][idx1:idx2+1], 1, full=True)
    p = np.poly1d(pol)
    slope, intercept, r_value, p_value, std_err = \
        stats.linregress(range(len(time[idx1:idx2+1])),
                               rfile[cdata][idx1:idx2+1])
    points['Slope (ppm/s)'][pt] = pol[0]
    points['Res'][pt] = res[0]
    points['R2'][pt] = r_value**2
    points['Flux (mmol/m2/d)'][pt] = pol[0]*Vol/(M*Area)*86.4
    points['FID'][pt] = pt + 1

    # Creation figures per flux
    figf = plt.figure(figsize=(7,5))
    axf = figf.add_subplot(111)
    cR2 = u'R$^2$ = %0.2f' % (r_value**2)
    cf = u'$f(x)$ = %0.2E$x$ + %0.2f' % (Decimal(pol[0]),pol[1])
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

    # save results in excel sheet of raw LGR data per flux
    rfile[cdata][idx1:idx2+1].to_excel(writer, sheet_name = 'FID_' + str(pt + 1), index = [0])
plt.close()

# Save final resutls in excel sheet
#points = points.set_index('Time')
points.to_excel(writer, sheet_name = 'Results')#, float_format='%.3f')
workbook = writer.book
worksheet = writer.sheets['Results']
sciformat = workbook.add_format({'num_format': '0.00E+0'})
floatformat = workbook.add_format({'num_format': '0.000'})
worksheet.set_column('I:I', None, sciformat)
worksheet.set_column('G:G', None, floatformat)
worksheet.set_column('H:H', None, floatformat)
worksheet.set_column('J:L', None, floatformat)
writer.save()
writer.close()

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
