#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 7 13:35:00 2021

@author: mensanli

last update: 01-07-2021
"""

import os
import re


def create_station_json(stations_lib='station.txt', station_list='station_list.txt', json_file='station_list.json'):
    """"
Create station_list.json from
    :rtype: object
    :param stations_lib：.txt include all stations info
    :param station_list: .txt stations selected
    :param json_file: reform in .json
    """

    args = dict(stations_lib=stations_lib, station_list=station_list, json_file=json_file)

    json_dir = os.path.join(os.getcwd(), args['json_file'])
    ex_files = open(json_dir, 'w')
    ex_files.write("{")
    ex_files.close()
    slist = open(args['station_list'])
    stations_sel = slist.readlines()
    count = len(stations_sel)
    print(count)
    n = 0
    for line in stations_sel:
        # stations = line.strip('\n')
        stations = line.split()[1]
        #print(stations)
        lib = open(args['stations_lib'])
        libs = lib.readlines()
        n += 1
        print(n)
        for lines in libs:
            net = lines.split()[0]
            sta = lines.split()[1]
            lon = lines.split()[2]
            lat = lines.split()[3]
            alt = lines.split()[4]

            if sta == stations:
                print(stations)
                if n <= count - 1:

                    json_dics = '"{}": {{"network": "{}", "channels": ["BHZ", "BHE", "BHN"], "coords": [{}, {}, ' \
                                '{}]}}, '.format(sta, net, lon, lat, alt)
                    print(json_dics)
                    ex_files2 = open(json_dir, 'r+')
                    ex_files2.read()
                    ex_files2.write(json_dics)
                    ex_files2.close()
                else:
                    json_dics = '"{}": {{"network": "{}", "channels": ["BHZ", "BHE", "BHN"], "coords": [{}, {}, ' \
                                '{}]}}'.format(sta, net, lon, lat, alt)
                    print(json_dics)
                    ex_files2 = open(json_dir, 'r+')
                    ex_files2.read()
                    ex_files2.write(json_dics)
                    ex_files2.close()

    ex_files3 = open(json_dir, 'r+')
    ex_files3.read()
    ex_files3.write("}")
    ex_files3.close()
