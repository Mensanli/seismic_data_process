# reshape temp-phs ----->  B001 1 stationlat stationlon stationalt eventlat  origintime Pg/Sgtime  ...
# 2021.6.9 @msl
# last mod: 2021.10.11

from obspy.core import UTCDateTime
import os

stations_lib="sta.txt"  # YN BAS 25.12 99.15 1675
phs_file="YB_2021.phs" #  stan info: " # 2021 1 1 12 48 39.54 26.1688 99.8688 8.9 0.00 0 0 0 1 20210101124839 eq " ; arrivel info: " BCB012 8.61 1 Pg "            
phs_data="phase_info.dat"

fs=open(stations_lib,'r')
ff=open(phs_file,'r')
latdic=[]
londic=[]
altdic=[]
for i in fs.readlines():
    i=i.strip("\n").split(" ")
    while '' in i:
        i.remove('')    
    list_lat=i[1:3:1]
    list_lon=i[1:4:2]
    #print(list_lon)
    list_alt=i[1:5:3]
    #print(list_lat)
    latdic.append(list_lat)
    londic.append(list_lon)
    altdic.append(list_alt)
latdic=dict(latdic)
londic=dict(londic)
altdic=dict(altdic)
#print(latdic["YUL"])

with open('_temp3.phs','wt') as fo:
    for line in ff.readlines():
        line=line.strip("\n")
        line=line.split(" ")
        if line[0]=="#":
            oyear=line[1]
            omonth=line[2]
            oday=line[3]
            ohour=line[4]
            ominu=line[5]
            osecend=line[6]
            osec1=osecend.split(".")[0]
            osec2=osecend.split(".")[1]
            eventlat=line[7]
            eventlon=line[8]
            eventdep=line[9]
            eventmag=line[10]
            evid=line[14]
            tt="{}-{}-{}T{}:{}:{}".format(oyear,omonth,oday,ohour,ominu,osecend)
            oTime=UTCDateTime(tt)
            ojulday=oTime.julday
            #print(oTime,ojulday)
            m1=line[0]
        else:
            net=line[0][:2]
            station=line[0][2:]
            pick=line[1]
            pha=line[3]
            #match=line[0]
            #print(line[0],evid,latdic[station],londic[station],altdic[station],oyear,ojulday,ohour,ominu,osec1,osec2,eventlat,eventlon,eventdep,pick,pha)
            if pha=="Pg":
                fo.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(line[0],evid,latdic[station],londic[station],altdic[station],oyear,ojulday,ohour,ominu,osec1,osec2,eventlat,eventlon,eventdep,pick,pha,"none Sg"))
            else:
                fo.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(line[0],evid,latdic[station],londic[station],altdic[station],oyear,ojulday,ohour,ominu,osec1,osec2,eventlat,eventlon,eventdep,"none Pg",pick,pha)) 
fo.close()

fe=open(r'_temp3.phs','r')
with open('_temp4.phs','wt') as fb:
    item=fe.readline()
    item=item.strip("\n")
    item=item.split(" ")
    print(item)
    mstation=item[0]
    mevid=item[1]
    mpha=item[-1]
    mpick=item[-2]
    mpha0=item[-3]
    mpick0=item[-4]
    show1=' '.join(item)
 #   print(show1)
    fb.write("{}\n".format(show1))
    for bb in fe.readlines():
        bb=bb.strip("\n")
        bb=bb.split(" ")
        show0=' '.join(bb)
#        print(show0)
        show="{} {} {} {} {} {} {} {} {} {}  {} {} {} {}".format(bb[0],bb[1],bb[2],bb[3],bb[4],bb[5],bb[6],bb[7],bb[8],bb[9],bb[10],bb[11],bb[12],bb[13])
        if bb[0]==mstation and bb[1]==mevid and bb[-2]==mpick:
#            print(show1)
            fb.write("{}\n".format(show1))
        if bb[0]==mstation and bb[1]==mevid and bb[-2]!=mpick:
            if bb[-2]=="none":
#                print(show,bb[-4],bb[-3],mpick,mpha)
                fb.write("{} {} {} {} {}\n".format(show,bb[-4],bb[-3],mpick,mpha))
            else:
#                print(show,mpick0,mpha0,bb[-2],bb[-1])
                fb.write("{} {} {} {} {}\n".format(show,mpick0,mpha0,bb[-2],bb[-1]))

        else:
#            print(show0)
            fb.write("{}\n".format(show0))
            mstation=bb[0]
            mevid=bb[1]
            mpick=bb[-2]
            mpha=bb[-1]
            mpick0=bb[-4]
            mphs0=bb[-3]
            show0=' '.join(bb)
fb.close()

fe2=open(r'_temp4.phs','r')
double_phs=[]
for ttt in fe2.readlines():
    ttt=ttt.strip("\n").split(" ")
    if ttt[-4]!="none" and ttt[-2]!="none":
        list_double=ttt[0]+ttt[1]
        double_phs.append(list_double)
    else:
        continue
#print(double_phs)
fe2.close()
fe3=open(r'_temp4.phs','r')        
with open(phs_data,'wt') as fd:
    for temp in fe3.readlines():
        temp=temp.strip("\n")
        temp=temp.split(" ")
        while '' in temp:
            temp.remove('')
        #print(temp[0])
        idea_i=temp[0]+temp[1]
        #print(idea_i)
        if temp[-4]=="none" or temp[-2]=="none":
            may_single=','.join(temp)  
            if idea_i not in double_phs:
                print("singe_______")
                fd.write("{}\n".format(may_single))

        elif temp[-4]!="none" and temp[-2]!="none":
            may_double=','.join(temp)    
            if idea_i in double_phs:
                print("______double")
                fd.write("{}\n".format(may_double))    
fd.close()
os.remove("_temp4.phs")
os.remove("_temp3.phs")
