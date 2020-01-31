import requests
import re
import json
import time
from bs4 import BeautifulSoup

class data_t:
    def __init__(self,loadstr="",name="",province="",confirmed=0,suspected=0,cured=0,dead=0):
        if loadstr=="":
            self.name=name
            self.province=province
            self.confirmed=confirmed
            self.suspected=suspected
            self.cured=cured
            self.dead=dead
        else:
            lst=sz.split(',')
            self.province=lst[0]
            self.name=lst[1]
            self.confirmed=int(lst[2])
            self.suspected=int(lst[3])
            self.cured=int(lst[4])
            self.dead=int(lst[5])
    def save(self):
        sz=self.province+','
        sz+=self.name+','
        sz+=str(self.confirmed)+','
        sz+=str(self.suspected)+','
        sz+=str(self.cured)+','
        sz+=str(self.dead)+'\n'
        return sz
        
    def __eq__(self,other):
        if not isinstance(other,data_t):
            return False
        return self.confirmed==other.confirmed and self.cured==other.cured and self.dead==other.dead and self.suspected==other.suspected
    def __str__(self):
        sz=self.province+self.name
        sz+="  "*(10-len(sz))
        return "%s    确诊：%4d    疑似：%4d    治愈：%4d    死亡：%4d"%(sz,self.confirmed,self.suspected,self.cured,self.dead)

url="https://3g.dxy.cn/newh5/view/pneumonia_peopleapp"
waiting=[1,1,1,1,1,10,60,600]

while True:
    t=time.localtime()
    t="%d-%d-%d %02d:%02d:%02d"%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
    plst={}
    try:
        with open("d:\\lastdata.txt","r") as f:
            tmp=f.readlines()
            for sz in tmp:
                data=data_t(loadstr=sz)
                plst[(data.province,data.name)]=data
    except:
        pass


    for w in waiting:
        try:
            ret=requests.get(url)
            ret.encoding='utf-8'
            with open("d:\\last_data.txt","w") as f:
                f.write(ret.text)
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

    lst={}
    for p in data:
        pd=data_t(province=p["provinceShortName"])
        for c in p["cities"]:
            d=data_t(name=c['cityName'],confirmed=c['confirmedCount'],suspected=c['suspectedCount'],cured=c['curedCount'],dead=c['deadCount'],province=pd.province)
            lst[(d.province,d.name)]=d

    with open("d:\\lastdata.txt","w") as f:
        for d in lst.values():
            f.write(d.save())


    log=[]
    for it in lst.items():
        this=it[1]
        pre=plst.get(it[0],None)
        if pre==None:
            continue
        if this==pre:
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
        log.append(sz)

    if len(log)>0:
        log.insert(0,t)
        with open("d:\\新增病例.txt",'a') as f:
            for sz in log:
                f.write(sz+'\n')
            f.write("=========================================================================\n")
    print('\r',end='')
    if len(log)==0:
        pass
    print(log)
    
    time.sleep(300)
