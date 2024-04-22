from bs4 import BeautifulSoup
import requests
from csv import writer

state=input("Enter the state: ")
district=input("Enter the district: ")
if(state=="ARUNACHAL PRADESH"):
    state='ARUNACHAL+PRADESH'
elif(state=='ANDHRA PRADESH'):
    state='ANDHRA+PRADESH'
elif(state=='DAMAN & DIU'):
    state='DAMAN+%26+DIU'
elif(state=='HIMACHAL PRADESH'):
    state='HIMACHAL+PRADESH'
elif(state=='JAMMU & KASHMIR'):
    state='JAMMU+%26+KASHMIR'
elif(state=='MADHYA PRADESH'):
    state='MADHYA+PRADESH'
elif(state=='UTTAR PRADESH'):
    state='UTTAR+PRADESH'
elif(state=='WEST BENGAL'):
    state='WEST+BENGAL'


html_text=requests.get("https://nmba.dosje.gov.in/photo-gallery-dashboard.php?state="+state+"&district="+district+"&filter=#").text


soup=BeautifulSoup(html_text,'lxml')
lists=soup.find_all('div',class_='h600')
fh=open('data.txt','w',encoding="utf-8")

for l in lists:
    s=l.text
    fh.write(s)
