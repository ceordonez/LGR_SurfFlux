#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config_file import *
from src.read_data import read_data
from src.plots import plot_select_points, plot_perflux, plot_alldata
from src.processing_data import processing_data
from src.write import write_excelres

def main():
    DataLGR = read_data(path_in, lake, date, txtfile)

    Pts_selected = plot_select_points(DataLGR, n)

    Results, p1, cdata = processing_data(Pts_selected, DataLGR, n, Temp, Press, Vol, Area,
                              var)
    plot_perflux(DataLGR, Results, p1, cdata, path_out, lake, txtfile, date, var)

    write_excelres(path_out, var, lake, txtfile, DataLGR, cdata, Results)

    plot_alldata(DataLGR, Results, path_out, lake, var, txtfile, date, cdata)

if __name__ == '__main__':
    main()
