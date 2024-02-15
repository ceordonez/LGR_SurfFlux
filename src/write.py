#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

def write_excelres(data, results, cdata, cfg):

    path_out = cfg['path_out']
    site = cfg['site']
    lgrfile = cfg['file']
    var = cfg['variable']

    # Creating folder for excel results if does not exist
    path_results = os.path.join(path_out, site , 'Results', 'LGR')
    if not os.path.exists(path_results):
        os.makedirs(path_results)

    # Cration of excel file and perform final calculations
    excel_filename = var + '_' + site + '_LGR_' + lgrfile + '.xlsx'
    excelpath = os.path.join(path_results, excel_filename)
    writer = pd.ExcelWriter(excelpath, datetime_format='mmm d yyyy hh:mm:ss',
                            engine='xlsxwriter')

    for pt in range(len(results)):
        # save results in excel sheet of raw LGR data per flux
        idx1 = results['ID start'][pt]
        idx2 = results['ID end'][pt]
        data[cdata][idx1:idx2+1].to_excel(writer, sheet_name = 'FID_' + str(pt + 1), index = [0])

    # Save final resutls in excel sheet
    results.to_excel(writer, sheet_name = 'Results')#, float_format='%.3f')
    workbook = writer.book
    worksheet = writer.sheets['Results']
    sciformat = workbook.add_format({'num_format': '0.00E+0'})
    floatformat = workbook.add_format({'num_format': '0.000'})
    worksheet.set_column('I:I', None, sciformat)
    worksheet.set_column('G:G', None, floatformat)
    worksheet.set_column('H:H', None, floatformat)
    worksheet.set_column('J:L', None, floatformat)
    writer._save()
