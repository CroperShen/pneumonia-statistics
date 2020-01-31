from class1 import TimeFunc
from random import randint
@TimeFunc
def func320(sz:str):
    dct={}
    for i in sz:
        dct[i]=dct.get(i,0)+1
    lst=list(dct.values())
    lst.sort(reverse=True)
    ret,pre=0,0xFFFFFFFF
    for i in lst:
        pre=max(0,min(i,pre-1))
        ret+=i-pre
    return ret


@TimeFunc
def func320_2(sz:str):
    lst=[0]*26
    for i in sz:
        lst[ord(i)-97]+=1
    lst.sort(reverse=True)
    ret,pre=0,0xFFFFFFFF
    for i in len(lst):
        pre=min(i,pre-1)
        ret+=i-pre
    return ret



for i in range(10):
    print(i)
    sz="".join(chr(97+randint(0,25)) for i in range(100000))
    func320(sz)
    func320_2(sz)
print(func320.GetAveRunTime())
print(func320_2.GetAveRunTime())

