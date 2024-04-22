import numpy as np
import pandas as pd
geo =  []
li =[]
for i in open('data.txt', errors="ignore"):
    if (i.split(":"))[0]=="Geo-coordinates":
        geo.append(i.split(":")[1].strip('\n'))

# we are taking geo coordinates as the base for the no. of the values
parti=[None]*len(geo)
prog = [None]*len(geo)
coll=[None]*len(geo)
#Now dividing the data according to the geo coordinates
l=[]
b=[]
f = open('data.txt',"r", errors="ignore")
d= f.readlines()
for i in d:
    if "Geo-coordinates" in i:
        b.append(l)
        l=[]
        continue
    else:
        l.append(i) 
#b contains divided data wrt the geo coordinates
lis=[]
j=[]
for line in b:
     for i in line:
       lis.append((i.split(":")))
     j.append(lis)
     lis=[] 
for ik in range(len(j)):
    for i in j[ik]:
        if i[0]=="Total Participants":
             parti[ik]=(int(i[1].strip('\n')))
        if i[0]=="Type of programme":
              prog[ik]=(i[1].strip('\n'))
        if i[0]=="College/University":
            coll[ik]=(i[1].strip('\n'))
        
data = {"Geo-coordinates":geo, "Total Participants":parti,"Type of programme":prog,"College/University":coll}
df = pd.DataFrame(data = data)
print(df)
l=df.loc[:,"Total Participants"]
cord=df.loc[:,"Geo-coordinates"]
type_program=df.loc[:,"Type of programme"]
college=df.loc[:,"College/University"]
from math import cos, asin, sqrt, pi

#All distance are in km
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def near_location(lon2,lat2):
    threshold_dist=1
    loc=[]
    i=0
    minimum=1e9
    index=-1
    n=len(cord)
    while(i<n):
        long=""
        lati=""
        j=0
        a=cord[i]
        while(a[j]!=','):
            lati=lati+a[j]
            j=j+1
        j=j+1
        while(j<len(cord[i])):
            long=long+a[j]
            j=j+1
        long=float(long)
        lati=float(lati)
        dist=distance(lati,long,lat2,lon2)
        loc.append(dist)
        if(dist<minimum):
            minimum=dist
            index=i
        i=i+1
    n=len(loc)
    threshold_parti=l[index]+50
    for i in range(0,n):
        if(abs(minimum-loc[i])<=threshold_dist):
            if(l[i]>=threshold_parti):
                threshold_parti=l[i]
                index=i
    return index
lat1=23.564532
long1=34.463524
min_index=near_location(long1,lat1)
print(min_index)
answer=[]
answer.append(cord[min_index])
answer.append(type_program[min_index])
if(college[min_index]!=None):
    answer.append(college[min_index])
print(answer)

def more_partication():
    n=len(l)
    maximum=-1
    index=-1
    for i in range(0,n):
        if(maximum<l[i]):
            maximum=l[i]
            index=i
    return index

index=more_partication()
answer=[]
answer.append(cord[index])
answer.append(l[index])
answer.append(type_program[index])
if(college[index]!=None):
    answer.append(college[index])
print(answer)