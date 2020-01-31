import time
class TimeFunc:
    def __init__(self,func):
        self.func=func
        self.cr=0
        self.rt=0.0

    def __call__(self,*args,**kwargs):
        t1=time.clock()*1000
        ret=self.func(*args,**kwargs)
        t2=time.clock()*1000
        self.rt+=t2-t1
        self.cr+=1
        return ret

    def GetAveRunTime(self):
        if (self.cr==0):
            return -1
        return self.rt/self.cr

    def clear(self):
        self.cr=0
        self.rt=0
