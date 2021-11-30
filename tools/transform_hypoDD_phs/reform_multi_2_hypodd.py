# reform different phsfile ---> hypoDD.phs 
# code @msl
# last mod 2021/11/29
# 
# mslphs (from hypoinvers): "# 2021 11 21 18 40 15.85 37.091 77.012 15 1.9 0.695 20211121184015 1"  "XJ AKZ 2021 11 21 18 40 24.82 S"
# tempphs (MFT): "# 2008 09 30 17 05 26.240 37.610 76.098 136 2.1 0 0 0.679969 1 XJ.200810010105.0003 eq"  "XJBCH 47.1 1.0 Pn -0.23"
# CSF: CENC catalog formate

from obspy.core import UTCDateTime
import argparse
from datetime import datetime
import datetime as time

def mslphs_DD(phsfile):
    f=open(phsfile,'r')
    for line in f.read().splitlines():
        item=line.split(" ")
        while '' in item:
            item.remove('')
        #print(item) 
        if len(item)>10:
            yea=item[1]
            mon=item[2]
            day=item[3]
            hour=item[4]
            minu=item[5]
            sec=item[6]
            origin_time=yea+"-"+mon+"-"+day+"T"+hour+":"+minu+":"+sec
            #print(origin_time)
            origin_time_str=str(origin_time)
            origin=UTCDateTime(origin_time_str)
            #print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%8.4f%7.1f%5.2f%6.2f%6.2f%6.2f%10s"%(item[0],yea,mon,day,hour,minu,float(sec),float(item[7]),float(item[8]),float(item[9]),float(item[10]),0,0,0,item[14]))
            print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%(item[0],yea,mon,day,hour,minu,float(sec),float(item[7]),float(item[8]),float(item[9]),float(item[10]),"0.00","0.00","0.00",item[13]))
        else:
            yea2=item[2]
            mon2=item[3]
            day2=item[4]
            hour2=item[5]
            minu2=item[6]
            sec2=item[7]
            phase_time=yea2+"-"+mon2+"-"+day2+"T"+hour2+":"+minu2+":"+sec2
            phase_time_str=str(phase_time)
            phase=UTCDateTime(phase_time_str)
            dd=phase-origin
            print("%-2s%-4s%9.2f%7.3f%4s"%(item[0],item[1],dd,1,item[8]))

def tempphs_DD(phsfile):
    f=open(phsfile,'r')
    for line in f.read().splitlines():
        item=line.split(" ")
        while '' in item:
         item.remove('')

        #print(item) 
        if item[0]=="#":
            #print(item)
            yea=item[1]
            mon=item[2]
            day=item[3]
            hour=item[4]
            minu=item[5]
            sec=item[6]
            #print(sec)
            #origin_time=yea+"-"+mon+"-"+day+"T"+hour+":"+minu+":"+sec
            #print(origin_time)
            #origin_time_str=str(origin_time)
            #origin=UTCDateTime(origin_time_str)
            #print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%8.4f%7.1f%5.2f%6.2f%6.2f%6.2f%10s"%(item[1],yea,mon,day,hour,minu,float(sec),float(item[8]),float(item[9]),float(item[10]),float(item[11]),0,0,0,item[15]))
            print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%(item[0],yea,mon,day,hour,minu,float(sec),float(item[7]),float(item[8]),float(item[9]),float(item[10]),"0.00","0.00","0.00",item[14]))
        else:
            print("%-6s%9.2f%7.3f%4s"%(item[0],float(item[1]),float(item[2]),item[3][:1]))

def CSFphs_DD(phsfile): # Beijing Time ---> UTC Time 
    f=open(phsfile,'r',encoding='gbk')
    n=6762
    for line in f.read().splitlines():
        item=line.split(" ")
        while '' in item:
            item.remove('')
        if len(item)>0:
            #print(item)
            if item[0]=="DBO" and item[7]=="ML":
                YMD=item[2].split("-")
                HMS=item[3].split(":")
                time_o=item[2]+"T"+item[3]
                #print(time_o)
                #origin_time_str=str(time_o)
                #origin=UTCDateTime(origin_time_str)   # Beijing Time
                time_o=datetime.strptime(time_o,"%Y-%m-%dT%H:%M:%S.%f")
                origin=time_o-time.timedelta(seconds=28800)
                n+=1
                nn=str(n)
                #print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%("#",YMD[0],YMD[1],YMD[2],HMS[0],HMS[1],float(HMS[2]),float(item[4]),float(item[5]),float(item[6]),float(item[8]),"0.00","0.00","0.00",nn))
                print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%("#",origin.year,origin.month,origin.day,origin.hour,origin.minute,float(origin.second),float(item[4]),float(item[5]),float(item[6]),float(item[8]),"0.00","0.00","0.00",nn))
            elif item[0]=="DBO" and item[6]=="ML":
                YMD=item[2].split("-")
                HMS=item[3].split(":")
                time_o=item[2]+"T"+item[3]
                #print(time_o)
                #origin_time_str=str(time_o)
                #origin=UTCDateTime(origin_time_str)
                time_o=datetime.strptime(time_o,"%Y-%m-%dT%H:%M:%S.%f")
                origin=time_o-time.timedelta(seconds=28800)
                n+=1
                nn=str(n)
                #print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%("#",YMD[0],YMD[1],YMD[2],HMS[0],HMS[1],float(HMS[2]),float(item[4]),float(item[5]),0,float(item[7]),"0.00","0.00","0.00",nn))
                print("%s%5s%3s%3s%4s%3s%6.2f%9.4f%9.4f%7.1f%6.2f%6s%6s%6s%10s"%("#",origin.year,origin.month,origin.day,origin.hour,origin.minute,float(origin.second),float(item[4]),float(item[5]),0,float(item[7]),"0.00","0.00","0.00",nn))
            elif item[0]=="DPB" and item[4]=="Pg" and item[1]=="XJ":
                net=item[1]
                station=item[2]
                #weight=item[5]
                pick="P"
                time_pick=item[7]+"T"+item[8]
                #p_time_str=str(time_pick)
                #pickp=UTCDateTime(p_time_str)
                time_pick=datetime.strptime(time_pick,"%Y-%m-%dT%H:%M:%S.%f")
                pickp=time_pick-time.timedelta(seconds=28800)
                dd=pickp-origin
                #print(dd)
                print("%-2s%-4s%9.2f%7.3f%4s"%(net,station,dd.total_seconds(),1,pick))
            elif item[0]=="DPB" and item[5]=="Pg" and item[1]=="XJ":
                net=item[1]
                station=item[2]
                #weight=item[5]
                pick="P"
                time_pick=item[8]+"T"+item[9]
                #p_time_str=str(time_pick)
                #pickp=UTCDateTime(p_time_str)
                time_pick=datetime.strptime(time_pick,"%Y-%m-%dT%H:%M:%S.%f")
                pickp=time_pick-time.timedelta(seconds=28800)
                dd=pickp-origin
                #print(dd)
                print("%-2s%-4s%9.2f%7.3f%4s"%(net,station,dd.total_seconds(),1,pick))

            elif item[0]=="DPB" and item[4]=="Sg" and item[1]=="XJ":
                net=item[1]
                station=item[2]
                #weight=item[5]
                pick="S"
                time_pick=item[7]+"T"+item[8]
                #s_time_str=str(time_pick)
                #picks=UTCDateTime(s_time_str)
                time_pick=datetime.strptime(time_pick,"%Y-%m-%dT%H:%M:%S.%f")
                picks=time_pick-time.timedelta(seconds=28800)
                dd=picks-origin
                print("%-2s%-4s%9.2f%7.3f%4s"%(net,station,dd.total_seconds(),1,pick))
            elif item[0]=="DPB" and item[5]=="Sg" and item[1]=="XJ":
                net=item[1]
                station=item[2]
                #weight=item[5]
                pick="S"
                time_pick=item[8]+"T"+item[9]
                #s_time_str=str(time_pick)
                #picks=UTCDateTime(s_time_str)
                time_pick=datetime.strptime(time_pick,"%Y-%m-%dT%H:%M:%S.%f")
                picks=time_pick-time.timedelta(seconds=28800)
                dd=picks-origin
                print("%-2s%-4s%9.2f%7.3f%4s"%(net,station,dd.total_seconds(),1,pick))
        else:
            continue

def sel_reform_method():
    parser = argparse.ArgumentParser()
    parser.prog = 'Transform .phs to hypodd.phs'
    parser.description = 'please enter parameters type filename and outfile_name ...'
    parser.add_argument("-t", "--type", help="phsfile type (1==>mslphs; 2==>tempphs; 3==>CSFphs)",  type=str, default="0")
    parser.add_argument("-n", "--filename", help="phsfile name",  type=str, default="1")
    parser.add_argument("-o", "--outfile", help="phsfile name",  type=str, default="1")
    args = parser.parse_args()
   # print(args.type,args.filename)
    phstype = args.type
    phsfile = args.filename

    if phstype == "1":
        mslphs_DD(phsfile)
    elif phstype == "2":
        tempphs_DD(phsfile)
    elif phstype == "3":
        CSFphs_DD(phsfile)

if __name__ == '__main__':
    sel_reform_method() 
