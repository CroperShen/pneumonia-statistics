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
            lst=loadstr.split(',')
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
