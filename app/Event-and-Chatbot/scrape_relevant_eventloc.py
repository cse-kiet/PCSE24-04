from bs4 import BeautifulSoup
import requests
from csv import writer
import time

state_list=["ANDHRA PRADESH","ARUNACHAL PRADESH","ASSAM","BIHAR","CHANDIGARH","CHHATTISGARH","DAMAN & DIU","DELHI","GOA","GUJARAT","HARYANA","HIMACHAL PRADESH","JAMMU & KASHMIR","JHARKHAND","KARNATAKA","KERALA","MADHYA PRADESH","MAHARASHTRA","MANIPUR","MEGHALAYA","MIZORAM","NAGALAND","ODISHA","PUNJAB","RAJASTHAN","SIKKIM","TAMIL NADU","TRIPURA","UTTAR PRADESH","UTTARAKHAND","WEST BENGAL","TELANGANA"]
fh=open('record.txt','w',encoding="utf-8")
n=len(state_list)
final={}
for i in range(0,n):
    state=state_list[i]
    print(state)
    if(state_list[i]=="ARUNACHAL PRADESH"):
        state_list[i]='ARUNACHAL+PRADESH'
    elif(state_list[i]=='ANDHRA PRADESH'):
        state_list[i]='ANDHRA+PRADESH'
    elif(state_list[i]=='DAMAN & DIU'):
        state_list[i]='DAMAN+%26+DIU'
    elif(state_list[i]=='HIMACHAL PRADESH'):
        state_list[i]='HIMACHAL+PRADESH'
    elif(state_list[i]=='JAMMU & KASHMIR'):
        state_list[i]='JAMMU+%26+KASHMIR'
    elif(state_list[i]=='MADHYA PRADESH'):
        state_list[i]='MADHYA+PRADESH'
    elif(state_list[i]=='UTTAR PRADESH'):
        state_list[i]='UTTAR+PRADESH'
    elif(state_list[i]=='WEST BENGAL'):
        state_list[i]='WEST+BENGAL'

    l=[]
    while True:
        lr=[]
        district=input("Enter the district: ")
        lr.append(district)
        if district.find(' ') != -1:
            length=len(district)
            ind=-1
            for i in range(0,length):
                if(district[i]==' '):
                    ind=i
                    break
            district = list(district)
            district[ind] = '+'
            ''.join(district)
            district=str(district[0])
        html_text=requests.get("https://nmba.dosje.gov.in/photo-gallery-dashboard.php?state="+state_list[i]+"&district="+district+"&filter=#").text
        soup=BeautifulSoup(html_text,'lxml')
        activities=soup.find_all('span',class_='counter1 count')
        lr.append(int(activities[3].text))
        l.append(lr)
        final[state]=l
        flag=input("Enter:")
        if(flag=='n'):
            print(final)
            break
print(final)
    
