#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 10:23:00 2020

@author: mensanli

last update: 02-01-2021
"""
import os
import re
import shutil
from obspy.core import UTCDateTime


def linkage(source_dir='orig_data',
            stations="station_list.txt",
            study_start='2017-01-01',
            study_end='2017-01-03',
            link_dir='project1_mseed') -> object:
    """
To select stations & study time in data structure 730: NOTE: select waves in 1 year & single network
    :param source_dir: which data source '/data/seis2/pub/waves/' in r730
    :param stations: save in "station_list.json"
    :param study_start: zoom study time begin
    :param study_end: zoom study time end
    :param link_dir: 'project*_mseed/stations(independent folds)/network.station..BH?__start-time__end-time.mseed'
    :return: a dict link
    """

    args = dict(source_dir=source_dir, stations=stations, study_start=study_start, study_end=study_end,
                link_dir=link_dir)
    print(link_dir)
    start_t = UTCDateTime(args['study_start'])
    end_t = UTCDateTime(args['study_end'])
    start_jul = str(start_t.julday)
    end_jul = str(end_t.julday)
    # end_jul_p = int(end_jul) + 1
    years = str(start_t.year)
    print('The study time start from ' + years + ',' + start_jul + ' to ' + years + ',' + end_jul)
    out_linkdir = os.path.join(os.getcwd(), str(args['link_dir']))
    if os.path.isdir(out_linkdir):
        print('============================================================================')
        print(f' *** {out_linkdir} already exists!')
        inp = input(
            ' --> Type (Yes or y) to create a new empty directory! This will erase your previous results so make a '
            'copy if you want them.')
        if inp.lower() == "yes" or inp.lower() == "y":
            shutil.rmtree(out_linkdir)
            os.makedirs(out_linkdir)
        else:
            print("Okay.")
            return
    # make dir of each stations in use
    f1 = open(args['stations'])
    stationslist = f1.readlines()
    print(stationslist)
    schn = ["BHZ", "BHE"]
    for line in stationslist:
        #st = line.strip('\n')  # rm '\n'
        net = line.split()[0]
        st = line.split()[1]
        station_dir = os.path.join(out_linkdir, str(st))
        print(st)
        if os.path.isdir(station_dir):
            shutil.rmtree(station_dir)
        os.makedirs(station_dir)

        # files in use
        source_zoom = "{}/{}/{}/{}/{}".format(os.getcwd(), args['source_dir'], years, net, str(st))
        print(source_zoom)

        for i, e, o in os.walk(source_zoom):
            for files in o:
                src = os.path.join(i, files)
                src_file = re.split('/', src)[11]
                chn = src_file.split('.')[3]
                yea = int(src_file.split('.')[5])
                # print(yea)
                jul = int(src_file.split('.')[-1])
                if int(jul) >= start_t.julday and jul <= end_t.julday and chn in schn:
                    print(jul)
                    t0 = UTCDateTime(year=yea, julday=jul, precision=0)
                    print(t0)
                    t2 = str(UTCDateTime(t0 + 86400, precision=0))
                    t1 = str(t0)
                    nt1 = re.split('-|:', t1)
                    nt2 = re.split('-|:', t2)
                    # print(nt2)
                    dst = "{}/{}/{}/{}.{}..{}__{}{}{}{}{}__{}{}{}{}{}.mseed".format(os.getcwd(), str(args['link_dir']),
                                                                                    src_file.split('.')[1],
                                                                                    net,
                                                                                    src_file.split('.')[1], chn, nt1[0],
                                                                                    nt1[1],
                                                                                    nt1[2], nt1[3], nt1[4], nt2[0],
                                                                                    nt2[1],
                                                                                    nt2[2], nt2[3], nt2[4])
                    print(src)
                    print(dst)
                    os.symlink(src, dst)
