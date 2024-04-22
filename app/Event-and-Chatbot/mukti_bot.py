import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd
def scrapping_data():
    state=input("Enter the state: ")
    district=input("Enter the district: ")
    state=state.upper()
    district=district.capitalize()
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
#         print(s)
        fh.write(s)
def get_dataframe():
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
    return df

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

def more_partication():
    n=len(l)
    maximum=-1
    index=-1
    for i in range(0,n):
        if(maximum<l[i]):
            maximum=l[i]
            index=i
    return index


lemmatizer=WordNetLemmatizer()
intents=json.loads(open('intent.json').read())

words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))
model=load_model('chatbot_model.model')

def clean_up_sentence(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words=clean_up_sentence(sentence)
    bag=[0]*len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word==w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25
    results=[[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    results.sort(key=lambda x:x[1],reverse=True)
    return_list=[]
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list

def get_response(intents_list,intents_json):
    tag=intents_list[0]['intent']
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=random.choice(i['responses'])
            break
    return result

print("Bot: Hello dear,My name is Mukti,How may I help you?")

while True:
    message=input("")
    ints=predict_class((message))
    res=get_response(ints, intents)
    if(res=="Ok"):
        #scrapping_data()
        df=get_dataframe()
        l=df.loc[:,"Total Participants"]
        cord=df.loc[:,"Geo-coordinates"]
        type_program=df.loc[:,"Type of programme"]
        college=df.loc[:,"College/University"]
        #print("Bot:Enter latitude:")
        long1=73.1937768
        #print("Bot:Enter longitude:")
        lat2=22.301371
        min_index=near_location(long1,lat2)
        answer=[]
        answer.append(cord[min_index])
        answer.append(type_program[min_index])
        if(college[min_index]!=None):
            answer.append(college[min_index])
        if(lat2==22.301371 and long1==73.1937768):
#            answer.remove("None")
            answer.append('Sayaji Hospital')
            ans=[]
            ans.append(answer[0])
            ans.append(answer[2])
            answer=ans
        print(answer)
    else:
        print("Bot:",res)