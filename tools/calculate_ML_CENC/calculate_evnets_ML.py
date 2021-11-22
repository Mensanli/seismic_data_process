#2021.6.1 @msl
#calculate ML CENC 
#last: 2021.11.22

from obspy.core import UTCDateTime,read
import os
import re
import datetime
import subprocess
import math
import shutil
from numpy import *
import numpy as np
from math import radians, cos, sin, asin, sqrt
os.putenv("SAC_DISPLAY_COPYRIGHT", '0')

##### parameters ################################################
start_time="2021-01-01"
end_time="2021-05-30"
project_dir="event-waves"   # events_dir="20210521135347"  used in demo
RESP="RESP.all"
pzall="sac_PZs2"
# R13="R13.txt" # calib table  # Yunnan R13 Ruifeng Liu et al (2017)
sac_tmp="sac_tmp" # dir save the sac DD-1 temp (create in advance)
Ratio_ML="ML_ratio_table.txt" # reference eqs M>3.5
outfile="ML_results.txt"
#Pick_dir="Pick_0304-0530_48sta"

##### def_distance ##############################################
def haversine(lon1, lat1, lon2, lat2): 
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert to Radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # average r, km
    return c * r 

#####    run     ################################################
#eventdir=os.listdir(project_dir)

##### ML ML2  ML3   ################################################
with open(outfile,'w') as f:
    # Now begin
    project_events = os.listdir(project_dir)
    project_events.sort()
    for events_dir in project_events:
        print(events_dir)
        events_dir_back = os.path.join(sac_tmp, events_dir)
        if not os.path.exists(events_dir_back):
            os.mkdir(events_dir_back)
        else:
            print("This dir exist!")
        stations = []
        recru_events_dir = os.path.join(project_dir, events_dir)
        for schnnals in os.listdir(recru_events_dir):
            # print(schnnals)
            station = schnnals.split(".")[0]
            chn = schnnals.split(".")[1]
            # print(station)
            if chn == "N" or chn == "E":
                stations.append(station)
        stations.sort()
        stations = list(set(stations))
        print(stations)
        lML = []
        lML2 = []
        lML3 = []
        for station in stations:
            stationn = station + ".N.bp"
            statione = station + ".E.bp"
            stationz = station + ".Z.bp"
            waven = os.path.join(recru_events_dir, stationn)
            wavee = os.path.join(recru_events_dir, statione)
            wavez = os.path.join(recru_events_dir, stationz)
            # print(waven,wavee,wavez)

            # process sac DD-1
            s = "r ./{}/{}/{}.E.bp ./{}/{}/{}.N.bp ./{}/{}/{}.Z.bp \n".format(project_dir, events_dir, station,
                                                                              project_dir, events_dir, station,
                                                                              project_dir, events_dir,
                                                                              station)
            s += "ch LCALDA TRUE \n"
            # s += "wh\n"
            s += "trans from evalresp fname {} to none freq 0.05 1 10 18 \n".format(RESP)
            s += "trans from none to polezero s {} \n".format(pzall)
            s += "markptp length 5.0 to t9 \n"
            s += "w append .dd \n"
            s += "q \n"
            subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

            # process sac ptp
            s = "r ./{}/{}/{}.E.bp ./{}/{}/{}.N.bp ./{}/{}/{}.Z.bp \n".format(project_dir, events_dir, station,
                                                                              project_dir, events_dir, station,
                                                                              project_dir, events_dir,
                                                                              station)
            s += "markptp length 5.0 to t9 \n"
            s += "w append .ptp \n"
            s += "q \n"
            subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

            # move *.dd
            stationndd = station + ".N.bp.dd"
            stationedd = station + ".E.bp.dd"
            stationzdd = station + ".Z.bp.dd"
            wavendd = os.path.join(recru_events_dir, stationndd)
            waveedd = os.path.join(recru_events_dir, stationedd)
            wavezdd = os.path.join(recru_events_dir, stationzdd)

            wavendd_1 = os.path.join(events_dir_back, stationndd)
            waveedd_1 = os.path.join(events_dir_back, stationedd)
            wavezdd_1 = os.path.join(events_dir_back, stationzdd)
            # print(wavendd_1,waveedd_1,wavezdd_1)

            if not os.path.isfile(wavendd_1) and os.path.isfile(wavendd):
                shutil.move(wavendd, events_dir_back)
            else:
                print(wavendd_1, "exist !")
            if not os.path.isfile(waveedd_1) and os.path.isfile(waveedd):
                shutil.move(waveedd, events_dir_back)
            else:
                print(waveedd_1, "exist !")
            if not os.path.isfile(wavezdd_1) and os.path.isfile(wavezdd):
                shutil.move(wavezdd, events_dir_back)
            else:
                print(wavezdd_1, "exist !")

            # move *.ptp
            stationnptp = station + ".N.bp.ptp"
            stationeptp = station + ".E.bp.ptp"
            stationzptp = station + ".Z.bp.ptp"
            wavenptp = os.path.join(recru_events_dir, stationnptp)
            waveeptp = os.path.join(recru_events_dir, stationeptp)
            wavezptp = os.path.join(recru_events_dir, stationzptp)

            wavenptp_1 = os.path.join(events_dir_back, stationnptp)
            waveeptp_1 = os.path.join(events_dir_back, stationeptp)
            wavezptp_1 = os.path.join(events_dir_back, stationzptp)

            if not os.path.isfile(wavenptp_1) and os.path.isfile(wavenptp):
                shutil.move(wavenptp, events_dir_back)
            else:
                print(wavenptp_1, "exist !")
            if not os.path.isfile(waveeptp_1) and os.path.isfile(waveeptp):
                shutil.move(waveeptp, events_dir_back)
            else:
                print(waveeptp_1, "exist !")
            if not os.path.isfile(wavezptp_1) and os.path.isfile(wavezptp):
                shutil.move(wavezptp, events_dir_back)
            else:
                print(wavezptp_1, "exist !")

            try:
                # read wave info
                ste = read(waveedd_1)
                tre = ste[0]
                # tre.detrend('demean')
                # tre.detrend('linear')
                # tre.filter(type="bandpass",freqmin=0.2,freqmax=10.0,zerophase=True)
                datatre = tre.data
                # print(datatre)
                dist = tre.stats.sac["dist"]
                ptpe = tre.stats.sac["user0"]
                lat = tre.stats.sac["evla"]
                lon = tre.stats.sac["evlo"]
                # print(ptpe)

                stn = read(wavendd_1)
                trn = stn[0]
                datatrn = trn.data
                ptpn = trn.stats.sac["user0"]
                lat = trn.stats.sac["evla"]
                lon = trn.stats.sac["evlo"]
                # print(lat,lon)

                # calculate the max amp of n / e chnnal
                on_c = [x + 5 for x in range(0, 290, 5)]
                off_c = [y + 5 for y in range(5, 295, 5)]
                i = 0
                lamplitude = []
                while (i < len(on_c)):
                    on = on_c[i]
                    off = off_c[i]
                    amp = (max(abs(datatre[on:off])) + max(abs(datatrn[on:off]))) * 500000
                    lamplitude.append(amp)
                    i += 1
                ##print(max(lamplitude))

                # calculate ML:
                if dist <= 10:
                    Rd = 2
                elif dist > 10 and dist <= 15:
                    Rd = 2.1
                elif dist > 15 and dist <= 20:
                    Rd = 2.2
                elif dist > 20 and dist <= 25:
                    Rd = 2.4
                elif dist > 25 and dist <= 30:
                    Rd = 2.6
                elif dist > 30 and dist <= 35:
                    Rd = 2.7
                elif dist > 35 and dist <= 40:
                    Rd = 2.8
                elif dist > 40 and dist <= 45:
                    Rd = 2.9
                elif dist > 45 and dist <= 50:
                    Rd = 3.0
                elif dist > 50 and dist <= 55:
                    Rd = 3.1
                elif dist > 55 and dist <= 70:
                    Rd = 3.2
                elif dist > 70 and dist <= 85:
                    Rd = 3.3
                elif dist > 85 and dist <= 100:
                    Rd = 3.4
                elif dist > 100 and dist <= 120:
                    Rd = 3.5
                elif dist > 120 and dist <= 140:
                    Rd = 3.6
                elif dist > 140 and dist <= 160:
                    Rd = 3.7
                elif dist > 160 and dist <= 180:
                    Rd = 3.8
                elif dist > 180 and dist <= 220:
                    Rd = 3.9
                elif dist > 220 and dist <= 250:
                    Rd = 4.0
                # Rd=3
                ML = math.log10(max(lamplitude)) + Rd
                lML.append(ML)
                print("ML: ", station, dist, ML)
                print(ptpe, ptpn)
                print(type(ptpe))
                ML2 = math.log10((ptpe + ptpn) * 500000) + Rd
                lML2.append(ML2)
                print("ML2: ", station, dist, ML2)
            except:
                print("No data read in")

            # find the min dist event_ref ,then read ptp and move to sac_tmp dir
            Dist = 10  # distance limit
            for ML_table in open(Ratio_ML, 'r'):
                ML_table = ML_table.strip("\n")
                ML_table = ML_table.split(" ")
                event_ref = ML_table[1]
                MLs = ML_table[2]
                lat_ref = ML_table[5]
                lon_ref = ML_table[6]
                # print(event_ref,MLs,lat_ref,lon_ref)
                # if event_ref != events_dir:
                pair_distance = haversine(float(lon_ref), float(lat_ref), float(lon), float(lat))
                if pair_distance < Dist:
                    Dist = pair_distance
                    Event = event_ref
                else:
                    continue
            try:
                print("Dist: ", Dist, "Event: ", Event)
                events_dir_back_2 = os.path.join(sac_tmp, Event)
                if not os.path.exists(events_dir_back_2):
                    os.mkdir(events_dir_back_2)
                else:
                    print("This dir exist!")

                recru_Event = os.path.join(project_dir, Event)
                # find stations in Event
                station_ref_list = []
                for items in os.listdir(recru_Event):
                    station_ref_list.append(items.split(".")[0])
                station_ref_list.sort()
                station_ref_list = list(set(station_ref_list))
                match = 0

                for station_ref in station_ref_list:
                    # print(station, station_ref)
                    if station_ref == station:
                        print("yes,then calculate ratio")
                        match += 1
                        wavee_ref = os.path.join(recru_Event, statione)
                        waven_ref = os.path.join(recru_Event, stationn)
                        wavez_ref = os.path.join(recru_Event, stationz)

                        # process sac ptp ref:
                        s = "r ./{}/{}.E.bp ./{}/{}.N.bp ./{}/{}.Z.bp \n".format(recru_Event, station, recru_Event,
                                                                                 station,
                                                                                 recru_Event, station)
                        s += "markptp length 5.0 to t9 \n"
                        s += "w append .ptp \n"
                        s += "q \n"
                        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

                        # make ref_sac_tmp and move
                        # the station?ptp is same
                        wavenptp_ref = os.path.join(recru_Event, stationnptp)
                        waveeptp_ref = os.path.join(recru_Event, stationeptp)
                        wavezptp_ref = os.path.join(recru_Event, stationzptp)
                        print(wavezptp_ref)

                        wavenptp_ref_1 = os.path.join(events_dir_back_2, stationnptp)
                        waveeptp_ref_1 = os.path.join(events_dir_back_2, stationeptp)
                        wavezptp_ref_1 = os.path.join(events_dir_back_2, stationzptp)

                        if not os.path.isfile(wavenptp_ref_1) and os.path.isfile(wavenptp_ref):
                            shutil.move(wavenptp_ref, events_dir_back_2)
                        else:
                            print(wavenptp_ref_1, "exist !")
                        if not os.path.isfile(waveeptp_ref_1) and os.path.isfile(waveeptp_ref):
                            shutil.move(waveeptp_ref, events_dir_back_2)
                        else:
                            print(waveeptp_ref_1, "exist !")
                        if not os.path.isfile(wavezptp_ref_1) and os.path.isfile(wavezptp_ref):
                            shutil.move(wavezptp_ref, events_dir_back_2)
                        else:
                            print(wavezptp_ref_1, "exist !")

                        # calculate ratio amplitude
                        try:
                            or_stn = read(wavenptp_1)
                            or_ste = read(waveeptp_1)
                            ref_stn = read(wavenptp_ref_1)
                            ref_ste = read(waveeptp_ref_1)

                            or_trn = or_stn[0]
                            or_tre = or_ste[0]
                            ref_trn = ref_stn[0]
                            ref_tre = ref_ste[0]

                        except:
                            print("no_or_ref_data_read_in")

                        or_ptpn = or_trn.stats.sac["user0"]
                        or_ptpe = or_tre.stats.sac["user0"]
                        ref_ptpn = ref_trn.stats.sac["user0"]
                        ref_ptpe = ref_tre.stats.sac["user0"]

                        # calculate
                        A = (or_ptpn + or_ptpe) / 2
                        A0 = (ref_ptpn + ref_ptpe) / 2
                        # ratio=A/A0
                        print(A, A0, MLs)
                        if A > 0 and A0 > 0:
                            ML3 = math.log10(A / A0) + float(MLs)  # ignore Rd
                            print("ML3: ", station, Dist, ML3)
                            lML3.append(ML3)
                        else:
                            print("A = 0 , please check it! ")

                    else:
                        continue

                if match == 0:
                    print("Can not find the reference event !")
            except:
                Event = "nan"
                print("No reference events in 10km")

        print(events_dir, "ML: ", mean(lML), "; ML2: ", mean(lML2), "; ML3: ", mean(lML3), Event)
        f.write("{} ML: {} ML2: {} ML3: {} by {} in {}\n".format(events_dir, mean(lML), mean(lML2), mean(lML3), Event, Dist))
f.close()
