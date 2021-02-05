#!/usr/bin/env python3
# -*- coding: utf-8 -*

import os
import re
from obspy import UTCDateTime
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# import matplotlib.ticker as ticher


def item_count(source_dir="waves", year=2019, stations="station_list.txt"):
    args = dict(source_dir=source_dir, year=year, stations=stations)
    f1 = open(args['stations'])
    stationl = f1.readlines()
    schn = ["BHE", "SHE", "HLE"]

    for lines in stationl:
        net = lines.split()[0]
        station = lines.split()[1]
        print(net)
        print(station)
        aim_dir = "{}/{}/{}/{}/{}".format(os.getcwd(), args['source_dir'], year, net, str(station))
        it_time = []  # make empty list of a single station
        i = 0  # count the
        # print(aim_dir)
        for root, dirs, files in os.walk(aim_dir):
            for file in files:
                aim_f = os.path.join(root, file)
                aim = re.split('/', aim_f)[-1]
                chn = aim.split('.')[3]
                if chn in schn:
                    time = int(aim.split('.')[-1])
                    jul_time = UTCDateTime(year=args['year'], julday=time, hour=12, precision=0)
                    date = str(jul_time)
                    # print(date)
                    it_time.append(date)
                    i += 1
    return i, it_time


def plot_continuity(num, collect):
    name = np.ones(num) + 1
    print(name)
    dates = np.array([datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ") for d in collect])
    print(dates)

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Data Continuity Graph")

    # format xaxis with 1 day intervals
    ax.get_xaxis().set_major_locator(mdates.DayLocator(interval=1))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y %m %d"))
    ax.scatter(dates, name, s=2)
    plt.savefig("continuity.png")
    # Set y axis
    plt.show()
