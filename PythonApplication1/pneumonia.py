import requests
import re
import json
import time
from bs4 import BeautifulSoup
from class2 import *


def save_data(data:list,path:str):
    while True:
        f=None
        try:
            f=open(path,"w")
            break
        except:
            if f!=None and f._checkClosed()==False:
                f.close()
            time.sleep(1)
            continue
    for i in data.values():
        f.write(i.save())
    f.close()

def get_saved_data(path):
    try:
        ret={}
        with open(path,"r") as f:
            tmp=f.readlines()
            for sz in tmp:
                data=data_t(loadstr=sz)
                ret[(data.province,data.name)]=data
        return ret
    except:
        return {}


def now():
    t=time.localtime()
    return "%d-%d-%d %02d:%02d:%02d"%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)


def get_lastest_data():
    url="https://3g.dxy.cn/newh5/view/pneumonia_peopleapp"
    waiting=[1,1,1,1,1,10,60,0]

    for w in waiting:
        try:
            ret=requests.get(url)
            ret.encoding='utf-8'
            data=BeautifulSoup(ret.text,"html.parser")
            for sz in data.body.find_all("script"):
                if sz.attrs.get('id',"")=="getAreaStat":
                    sz=str(sz.string)
                    break
            else:
                raise "Error"
            sz=re.findall('\[.*\]',sz)[0]
            data=json.loads(sz)
            break
        except:
            time.sleep(w)
            continue
    else:
        return {}

    ret={}
    for p in data:
        pd=data_t(province=p["provinceShortName"])
        for c in p["cities"]:
            d=data_t(name=c['cityName'],confirmed=c['confirmedCount'],suspected=c['suspectedCount'],cured=c['curedCount'],dead=c['deadCount'],province=pd.province)
            ret[(d.province,d.name)]=d
    return ret


def data_cmp(datapre:dict,datanow:dict):
    ret=[]
    for it in datanow.items():
        key,this=it
        pre=datapre.get(key,None)
        if pre==None or this==pre:
            continue
        sz=this.province+this.name
        if this.confirmed!=pre.confirmed:
            sz+="  新增确诊:%d(%d->%d)" % (this.confirmed-pre.confirmed,pre.confirmed,this.confirmed)
        if this.suspected!=pre.suspected:
            sz+="  新增疑似:%d(%d->%d)" % (this.suspected-pre.suspected,pre.suspected,this.suspected)
        if this.cured!=pre.cured:
            sz+="  新增疑似:%d(%d->%d)" % (this.cured-pre.cured,pre.cured,this.cured)
        if this.dead!=pre.dead:
            sz+="  新增死亡:%d(%d->%d)" % (this.dead-pre.dead,pre.dead,this.dead)
        ret.append(sz)
    return ret

def printlog(log:list):
    if (len(log)==0):
        print(now()+"  无变化")
    else:
        print(now())
        for sz in log:
            print(sz)

def savelog(log:list,path:str):
    while True:
        f=None
        try:
            f=open(path,"a")
            print('\r',end="正在保存文件...")
            break
        except:
            print('\r',end="无法保存文件，将在关闭文件后继续尝试保存")
            if f!=None and f._checkClosed()==False:
                f.close()
            time.sleep(5)
            continue
    f.write(now())
    for i in log:
        f.write(i+'\n')
    f.write("==============================================================\n")
    f.close()
    print('\r',"文件保存成功")



def wait_and_print(n):
    t1=t0=time.time()
    while t1-t0<n:
        print("\r",end="等待中，下次检查数据还剩%d秒          " % (n-t1+t0))
        t1=time.time()
        time.sleep(1)
    print("\r",end="                                    \r")

def main():
    data_path="d:\\lastdata2.txt"
    log_path="d:\\log2.txt"

    while True:
        datapre=get_saved_data(data_path)
        datanow=get_lastest_data()
        save_data(datanow,data_path)

        log=data_cmp(datapre,datanow)
        if len(log)==0:
            printlog(log)
        else:
            print("========================================================")
            printlog(log)
            savelog(log)
            print("========================================================")
        wait_and_print(120)

main()

