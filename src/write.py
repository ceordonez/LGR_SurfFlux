#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pandas as pd


def write_excelres(data, results, cfg):

    path_out = cfg["path_out"]
    site = cfg["site"]
    inputfile = cfg["file"]
    var = cfg["variable"]

    # Creating folder for excel results if does not exist
    path_results = os.path.join(path_out)
    if not os.path.exists(path_results):
        os.makedirs(path_results)

    # Cration of excel file and perform final calculations
    excel_filename = "_".join([var, site, inputfile + ".xlsx"])
    excelpath = os.path.join(path_results, excel_filename)
    writer = pd.ExcelWriter(
        excelpath, datetime_format="mmm d yyyy hh:mm:ss", engine="xlsxwriter"
    )

    if var == "CH4":
        vard = "[CH4]d_ppm"
    elif var == "CO2":
        vard = "[CO2]d_ppm"

    for pt in range(len(results)):
        # save results in excel sheet of raw LGR data per flux
        idx1 = results["ID start"][pt]
        idx2 = results["ID end"][pt]
        data[vard][idx1 : idx2 + 1].to_excel(
            writer, sheet_name="FID_" + str(pt + 1), index=[0]
        )

    # Save final resutls in excel sheet
    results.to_excel(
        writer, sheet_name="Results", index=False
    )  # , float_format='%.3f')
    workbook = writer.book
    worksheet = writer.sheets["Results"]
    dateformat = workbook.add_format({"num_format": "yyyy/mm/dd hh:mm"})
    sciformat = workbook.add_format({"num_format": "0.00E+0"})
    floatformat = workbook.add_format({"num_format": "0.000"})
    worksheet.set_column("D:E", None, dateformat)
    worksheet.set_column("H:H", None, sciformat)
    worksheet.set_column("F:F", None, floatformat)
    worksheet.set_column("G:G", None, floatformat)
    worksheet.set_column("I:K", None, floatformat)
    writer._save()
