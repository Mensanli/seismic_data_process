# **EQTransformer 流程：(GPU)**

**Create by Mensanli** 

**Last update: 2022-2-11**

**@518**

## 1. 启动 "z50_gpu" 环境

```bash
[xxx]$ conda activate z50_gpu
```

**该环境中已经安装好了EQTransformer  (set.py)**

**位置：**/home/mensanli/.conda/envs/eqt_z50/lib/python3.7/site-packages/EQTransformer-0.1.55-py3.7.egg/EQTransformer/utils

### 注：Tenserflow 与3090显卡兼容问题，需要关闭<u>并行</u>

**新版本环境：** 

## 2. 数据处理

### (1) 生成台站 .json

```bash
# 输入文件有以下两个：
# 1.台站信息 station_yc_json.txt
XJ HTTZ0 37.16 79.06 1592
XJ HTTZ1 37.1641 79.0595 1592
XJ HTTZ2 37.1608 79.054 1610
XJ HTTZ3 37.1695 79.0586 1580
XJ HTTZ4 37.162 79.0656 1615
XJ HTTZ5 37.1731 79.0722 1570
XJ HTTZ6 37.1586 79.0749 1603
XJ HTTZ7 37.1506 79.0575 1653
XJ HTTZ8 37.1616 79.0429 1622
XJ HTTZ9 37.1763 79.0522 1640
XJ YCH 37.39 77.361 2023
# 2.台站列表 station_list_yc.txt
XJ HTTZ0
XJ HTTZ1
XJ HTTZ2
XJ HTTZ3
XJ HTTZ4
XJ HTTZ5
XJ HTTZ6
XJ HTTZ7
XJ HTTZ8
XJ HTTZ9
XJ YCH
```

注：example中的.json结构是<u>先纬度后经度</u>

```python
import sys
sys.path.insert(0, '/home/mensanli/data_msl/Yutian-Works/eqtransformer-ref')

from EQTransformer.utils.json_maker import create_station_json
create_station_json(stations_lib='../station_yc_json.txt', station_list='../station_list_yc.txt', json_file='../station_list_stations_yc.json')
```

### (2) 波形事件选择 

```python
import sys
#sys.path.insert(0,'/data/seis3/work/data_msl/Yutian-Works/eqtransformer-ref')

from EQTransformer.utils.data_selecter import linkage

linkage(source_dir='/data/seis2/pub/waves',
        stations="../station_list_yc.txt",
        study_start='2021-01-01',
        study_end='2021-09-4',
        link_dir='../project_YC')
```

### (3) 开始预测

**直接使用mseed**

```python
from EQTransformer.core.mseed_predictor import mseed_predictor
mseed_predictor(input_dir='../project_YC_2021',
                input_model='/home/mensanli/data_msl/Yutian-Works/eqtransformer-ref/ModelsAndSampleData/EqT_model.h5',
                stations_json='../station_list_stations_yc.json',
                loss_weights=[0.02, 0.40, 0.58],
                output_dir='../detections_YC_2021',
                detection_threshold=0.3,
                P_threshold=0.1,
                number_of_plots=50,
                S_threshold=0.1,
                plot_mode='time_frequency',
                normalization_mode='std',
                batch_size=500,
                overlap=0.3,
                gpu_limit=None,
                gpuid=0)
```

**使用hdf5格式数据**

## 3. 事件关联

### 方法一：eqt关联



### 方法二：REAL

#### 1.arange_pick_XXX.sh

```sh
project_dir=/data/seis3/work/data_msl/Yecheng-Works/EQT_Yecheng/detections_YC_2021
for i in $(ls -l $project_dir | awk '{print $9}'| awk -F '_' '{print $1}' ) 
do
	echo $project_dir/$i"_outputs"/X_prediction_results.csv
	
       	awk -F ','  '{print $1","$2","$3","$12","$13","$16","$17}' $project_dir/$i"_outputs"/X_prediction_results.csv | awk -F ',' '$4>0 && NR>1 {print $1,$2,$3,$4,$5}'| awk '{print $1,$2,$3,$4"T"$5,$6,"0.0" }' | awk -F '[__ ]' '{print substr($3,1,8),$6,$7,$8,$9,$10}'  > $project_dir/$i"_outputs"/all_$i.P.txt
       	awk -F ',' '{print $1","$2","$3","$12","$13","$16","$17}' $project_dir/$i"_outputs"/X_prediction_results.csv | awk -F ',' '$6>0 && NR>1 {print $1,$2,$3,$6,$7}'| awk '{print $1,$2,$3,$4"T"$5,$6,"0.0" }' | awk -F '[__ ]' '{print substr($3,1,8),$6,$7,$8,$9,$10}'  > $project_dir/$i"_outputs"/all_$i.S.txt
       	
done
```

#### 2.create_picks_routine_XXX.py

```python
# 20210518 all stations ----> BC.B001.P.txt  BC.B012.P.txt ……
# The Picks file can create auto, but the aimfile overlape everytime!

from obspy.core import UTCDateTime
import os
import re
import datetime

##### parameters ################################################
start_time="2021-01-01"
end_time="2021-12-31"
detection_dir="/data/seis3/work/data_msl/Yecheng-Works/EQT_Yecheng/detections_YC_2021"
Pick_dir="Pick_Yecheng_2021"
#####    run     ################################################
startt=datetime.datetime.strptime(start_time,'%Y-%m-%d')
endtt=datetime.datetime.strptime(end_time,'%Y-%m-%d')
routt=startt
n=1
stations_dir=os.listdir(detection_dir)
deltatime=datetime.timedelta(days=n)
while (endtt-routt).days >=0:
    study_time=routt.strftime('%Y%m%d')
    out_dir=os.path.join(os.getcwd(),Pick_dir,study_time)
    print(study_time,out_dir)
    
    try:
        os.makedirs(out_dir)
    except:
        print("this dirs may be exist!")
    for station_dir in stations_dir:
        station=station_dir.split("_")[0]
        print(station)
        P_prediction="{}/{}/all_{}.P.txt".format(detection_dir,station_dir,station)
        f=open(P_prediction,'r')
        for line in f.readlines():
            pick=line.strip("\n")
            #print(pick)
            pick_time=pick.split()[0]
            #print(pick_time)
            pick_net=pick.split()[1]
            pick_P=pick.split()[3]
            #print(pick_P)
            pick_prob=pick.split()[4]
            pick_amp=pick.split()[5]
            travel_time_p=UTCDateTime(pick_P)-UTCDateTime(pick_time)
            aimfile="{}/{}.{}.P.txt".format(out_dir,pick_net,station)
            if pick_time.strip() == study_time:
                fo=open(aimfile,'a')
                print("write picks P to:",fo.name)
                P_picks="{} {} {}\n".format(travel_time_p,pick_prob,pick_amp)		
                fo.write(P_picks)
                #print(travel_time_p,pick_prob,pick_amp)
                fo.close()
        S_prediction="{}/{}/all_{}.S.txt".format(detection_dir,station_dir,station)
        f2=open(S_prediction,'r')
        for line2 in f2.readlines(): 
            pick2=line2.strip("\n")
            pick2_time=pick2.split()[0]
            pick2_net=pick2.split()[1]
            pick_S=pick2.split()[3]
            pick2_prob=pick2.split()[4]
            pick2_amp=pick2.split()[5]
            travel_time_s=UTCDateTime(pick_S)-UTCDateTime(pick2_time)
            aimfile2="{}/{}.{}.S.txt".format(out_dir,pick2_net,station)
            if pick2_time.strip() == study_time:
                fo2=open(aimfile2,'a')
                print("write picks S to:",fo2.name)
                S_picks="{} {} {}\n".format(travel_time_s,pick2_prob,pick2_amp)		
                fo2.write(S_picks)
                #print(travel_time_p,pick_prob,pick_amp)
                fo2.close()   

    routt=routt+deltatime
```

#### 3.run REAL

```sh
#!/usr/bin/sh
# associate phases one day step by REAL
# 2021.6.4 @msl

### dirs par #####################################################
station_lib=station_yc_json.txt
detections_dir=/home/mensanli/data_msl/association/detections_eqt
picks_lib=Pick_Yecheng_2021
results_dir=results_2021_Yecheng	
### REAL parameters ##############################################
# -D(nyear/nmon/nday/lat_center)
# latitude center is required to make lat. and lon. consistent in km
L="37.5"
# -R(rx/rh/tdx/tdh/tint[/gap/GCarc0/latref0/lonref0]])
# station gap constraint is strongly recommended when station coverage is poor
R="0.2/20/0.02/2/3/250/2"
# -G(trx/trh/tdx/tdh)  ( for heterogeneous layers)
#$G = "1.4/20/0.01/1"
# -V(vp0/vs0/[s_vp0/s_vs0/ielev])
V="6.2/3.3"
# -S(np0/ns0/nps0/npsboth0/std0/dtps/nrt[/rsel/ires])
S="3/2/5/2/0.5/0.2/1.5"
### run ###########################################################
mkdir $results_dir
for day in $(ls -l $detections_dir/$picks_lib | awk '{print $9}' )
do
	echo $day
	for station in $(ls -l $detections_dir/$picks_lib/$day | awk '{print $9}' | awk -F '.' '{print $2 }' | sort | uniq)
	do
	awk -v station_sel=$station '$2==station_sel {print $4,$3,$1,$2,"BHZ",$5/1000}' $station_lib >> _stations_pick.txt
	done
	#cat _stations_pick.txt
	echo "../bin/REAL" $day $L $R $V $S "_stations_pick.txt" $detections_dir/$picks_lib/$day | awk '{print $1, "-D"substr($2,1,4)"/"substr($2,5,2)"/"substr($2,7,2)"/"$3,"-R"$4,"-V"$5,"-S"$6,$7,$8 }' | sh
	echo "../bin/REAL" $day $L $R $V $S "_stations_pick.txt" $detections_dir/$picks_lib/$day | awk '{print $1, "-D"substr($2,1,4)"/"substr($2,5,2)"/"substr($2,7,2)"/"$3,"-R"$4,"-V"$5,"-S"$6,$7,$8 }'
	mv catalog_sel.txt $results_dir/$day"_catalog_sel.txt" 
	mv phase_sel.txt $results_dir/$day"_phase_sel.txt"
	rm _stations_pick.txt
done
```

#### 4.整理REAL结果

xxx (soon)

************

## 相关代码：

### ~/EQTransformer/utils/json_maker.py:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 7 13:35:00 2021

@author: mensanli

last update: 01-18-2021
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
        stations = line.split()[1]
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
```

### ~/EQTransformer/utils/data_selecter.py:

```python
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
            link_dir='project1_mseed'):
    """
To select stations & study time in data structure 730:
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
    schn = ["BHZ", "BHE", "BHN", "SHE", "SHZ", "SHN", "HLE", "HLN", "HLZ"]
    for line in stationslist:
        st = line.split()[1]
        net = line.split()[0]
        station_dir = os.path.join(out_linkdir, str(st))
        print(st)
        if os.path.isdir(station_dir):
            shutil.rmtree(station_dir)
        os.makedirs(station_dir)

    # files in use
        source_zoom = "{}/{}/{}/{}".format(args['source_dir'], years, net, str(st))
        print(source_zoom)

        for i, e, o in os.walk(source_zoom):
            for files in o:
                src = os.path.join(i, files)
                src_file = re.split('/', src)[-1]
                chn = src_file.split('.')[3]
                if chn in schn:
                    yea = int(src_file.split('.')[5])
            # print(yea)
                    jul = int(src_file.split('.')[-1])
                    if int(jul) >=start_t.julday and jul <= end_t.julday:
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
                                                                            src_file.split('.')[1], chn, nt1[0], nt1[1],
                                                                            nt1[2], nt1[3], nt1[4], nt2[0], nt2[1],
                                                                            nt2[2], nt2[3], nt2[4])
                        print(src)
                        print(dst)
                        os.symlink(src, dst)

```

