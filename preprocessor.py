import pandas as pd
import numpy as np
from datetime import datetime

def preprocessor(df,days,abc,start_,end_):
    df.drop(columns="Unnamed: 0", inplace=True)
    for i in range(1, df.shape[1]):
        df.iloc[:, i] = df.iloc[:, i].astype(int)
        df.iloc[:, i] = df.iloc[:, i].apply(lambda x: 'S' if x <= 4 else 'B')

    if days=="Last 10 days":
        df = df.iloc[:,0:11]
    elif days=="Last 7 days":
        df = df.iloc[:,0:8]
    elif days=="Any Particular Day":
        if abc != 'Select Date':
            df=df[['PERIOD',abc]]
    elif days=="Any Particular Weekday":
        if abc != 'Select Weekday':
            temp=[]
            for i in range(1,df.shape[1]):
                if abc==get_weekday(df.iloc[:,i].name):
                    temp.append(i)
            df=df.iloc[:,temp]

    time_duration = duration(start_, end_)
    if time_duration is None:
        return df
    else:
        df['start'] = df['PERIOD'].apply(start_1)
        df['start']=df['start'].astype(int)
        df=df[df['start'].isin(time_duration)]
        df.drop(columns=["start"],inplace=True)
        return df


def get_weekday(date_str):
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        # Get the weekday name
        weekday = date_obj.strftime('%A')
        return weekday
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."
def duration(s,e):
    if (s==None) | (e==None):
        if (s==None) & (e==None):
            return None
        elif s==None :
            e=int(e)
            return [e]
        elif e==None:
            s=int(s)
            return [s]
    else:
        s=int(s)
        e=int(e)
        time_duration=[]
        if s<e:
            for i in range(s,e):
                time_duration.append(i)
        else:
            while s<24:
                time_duration.append(s)
                s+=1
            for i in range(0,e):
                time_duration.append(i)
        return time_duration
def start_1(x):
    if (x >= 30) & (x <= 90):
        return "06"
    elif (x >= 91) & (x <= 150):
        return "07"
    elif (x >= 151) & (x <= 210):
        return "08"
    elif (x >= 211) & (x <= 270):
        return "09"
    elif (x >= 271) & (x <= 330):
        return "10"
    elif (x >= 331) & (x <= 390):
        return "11"
    elif (x >= 391) & (x <= 450):
        return "12"
    elif (x >= 451) & (x <= 510):
        return "13"
    elif (x >= 511) & (x <= 570):
        return "14"
    elif (x >= 571) & (x <= 630):
        return "15"
    elif (x >= 631) & (x <= 690):
        return "16"
    elif (x >= 691) & (x <= 750):
        return "17"
    elif (x >= 751) & (x <= 810):
        return "18"
    elif (x >= 811) & (x <= 870):
        return "19"
    elif (x >= 871) & (x <= 930):
        return "20"
    elif (x >= 931) & (x <= 990):
        return "21"
    elif (x >= 991) & (x <= 1050):
        return "22"
    elif (x >= 1051) & (x <= 1110):
        return "23"
    elif (x >= 1111) & (x <= 1170):
        return "00"
    elif (x >= 1171) & (x <= 1230):
        return "01"
    elif (x >= 1231) & (x <= 1290):
        return "02"
    elif (x >= 1291) & (x <= 1350):
        return "03"
    elif (x >= 1351) & (x <= 1410):
        return "04"
    else:
        return "05"




