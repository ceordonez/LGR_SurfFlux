#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from config_file import *
from src.read_data import read_data, read_config
from src.plots import plot_data
from src.processing_data import processing_data
from src.write import write_excelres

def main():

    cfg = read_config('config.yml')

    ## STEP 1: Read data
    data = read_data(cfg)

    ## STEP 2: Processing data
    results, p1 = processing_data(data, cfg)

    plot_data(data, results, p1, cfg)

    write_excelres(data, results, cfg)


if __name__ == '__main__':
    main()
