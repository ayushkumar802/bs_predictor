import re
import pandas as pd
import numpy as np
from datetime import datetime

def count_pattern_occurrences(string, pattern):
    matches = re.finditer(f"(?={pattern})", string)
    return sum(1 for _ in matches)

def pattern_table1(df,pattern):
    a=create_string(df)
    hehe=0
    if longest_repeating_sequence(a, pattern) is None:
        hehe="None"
    else:
        hehe=longest_repeating_sequence(a, pattern)
    temp={
        "Total Occurrence": round(count_pattern_occurrences(a, pattern)),
        "Contribution of this pattern in game": f"{round((count_pattern_occurrences(a,pattern)/((df.shape[0]/len(pattern))*(df.shape[1]-1)))*100,2)} %",
        "Longest Sequence of this Pattern": hehe
    }
    return temp

def pattern_table2(df,pattern):
    a=create_string(df)
    if pattern[-1] == "S":
        opposite= "B"
    else:
        opposite= "S"
    hehe=0
    if (count_pattern_occurrences(a, pattern)==0) & (count_pattern_occurrences(a, pattern[:-1] + opposite)==0):
        hehe=0
    else:
        hehe=round(count_pattern_occurrences(a, pattern) / (count_pattern_occurrences(a, pattern) + count_pattern_occurrences(a, pattern[:-1] + opposite)), 2)

    q,r=next_probablity(pattern,df)
    temp={
        "Winning probability if your next move is 'S'": q,
        "Winning probability if your next move is 'B'": r,
        f"Probability of getting {pattern[-1]} after {pattern[:-1]}": hehe
    }
    return temp

#     print(f"the Pattern: {ab}\nWinning probablity if your move is 'S': {q}\nWinning probablity if your move is 'B': {w}\n")
def pattern_bar(df,pattern):
    inv=""
    for i in pattern:
        if i=="S":
            inv+="B"
        else:
            inv+="S"
    temp=[]
    for i in range(1,df.shape[1]):
        a=""
        a="".join(df.iloc[:,i])
        name=df.iloc[:,i].name
        count1=count_pattern_occurrences(a, pattern)
        count2=count_pattern_occurrences(a, inv)
        temp.append((name,count1,count2))
    new_df=pd.DataFrame(temp)
    new_df.rename(columns={
        0:"date",
        1:pattern,
        2:inv
    },inplace=True)
    return new_df




def longest_repeating_sequence(string, pattern):
    max_length = 0
    current_length = 0
    i = 0
    n = len(string)

    while i < n - 1:
        # Check if the current substring matches the pattern
        if string[i:i + len(pattern)] == pattern:
            current_length += 1
            i += len(pattern)  # Move forward by the length of the pattern
        else:
            max_length = max(max_length, current_length)
            current_length = 0
            i += 1
    max_length = max(max_length, current_length)

    # Return the repeated pattern
    return pattern * max_length
def next_probablity(ab,df):
    try:
        a=create_string(df)
        if (count_pattern_occurrences(a,ab + "S") == 0) & (count_pattern_occurrences(a,ab + "B") == 0):
            return 0,0

        q=round(count_pattern_occurrences(a,ab + "S")/(count_pattern_occurrences(a,ab + "S")+count_pattern_occurrences(a,ab +"B")),2)
        w=round(count_pattern_occurrences(a,ab + "B")/(count_pattern_occurrences(a,ab + "S")+count_pattern_occurrences(a,ab +"B")),2)
        return q,w
    except ValueError:
        return 0



def create_string(df):
    a=""
    for i in range(1,df.shape[1]):
        a+="".join(df.iloc[:,i])
    return a



def analysis_24H(df,Pattern):
    a=[]
    for i in range(1,df.shape[1]):
        day="".join(df.iloc[:,i])
        a.extend(find_pattern_occurrences(day,Pattern))
    if len(a)==0:
        return None
    a=pd.DataFrame(a)
    a["period"]=a[0].apply(lambda x: time_(x))
    a=a.groupby("period").count().reset_index()
    return a



def find_pattern_occurrences(string, pattern):
    matches = re.finditer(f"(?={pattern})", string)
    return [match.start() for match in matches]

def time_(x):
    if (x>=30) & (x<=90):
        return "06-07"
    elif (x>=91) & (x<=150):
        return "07-08"
    elif (x>=151) & (x<=210):
        return "08-09"
    elif (x>=211) & (x<=270):
        return "09-10"
    elif (x>=271) & (x<=330):
        return "10-11"
    elif (x>=331) & (x<=390):
        return "11-12"
    elif (x>=391) & (x<=450):
        return "12-13"
    elif (x>=451) & (x<=510):
        return "13-14"
    elif (x>=511) & (x<=570):
        return "14-15"
    elif (x>=571) & (x<=630):
        return "15-16"
    elif (x>=631) & (x<=690):
        return "16-17"
    elif (x>=691) & (x<=750):
        return "17-18"
    elif (x>=751) & (x<=810):
        return "18-19"
    elif (x>=811) & (x<=870):
        return "19-20"
    elif (x>=871) & (x<=930):
        return "20-21"
    elif (x>=931) & (x<=990):
        return "21-22"
    elif (x>=991) & (x<=1050):
        return "22-23"
    elif (x>=1051) & (x<=1110):
        return "23-24"
    elif (x>=1111) & (x<=1170):
        return "00-01"
    elif (x>=1171) & (x<=1230):
        return "01-02"
    elif (x>=1231) & (x<=1290):
        return "02-03"
    elif (x>=1291) & (x<=1350):
        return "03-04"
    elif (x>=1351) & (x<=1410):
        return "04-05"
    else:
        return "05-06"




def analysis_week(df,Pattern):
    a=[]
    weeks=[]
    for i in range(1,df.shape[1]):
        day="".join(df.iloc[:,i])
        weekday=[get_weekday(df.iloc[:,i].name)]
        q=find_pattern_occurrences(day,Pattern)
        a.extend(q)
        weeks.extend(weekday*len(q))
    a=pd.DataFrame(a,columns=['num'])
    a['week']=weeks
    a["period"]=a['num'].apply(lambda x: time_(x))
    a_agg=a.groupby(['week','period'])['num'].count().reset_index()
    pivot_table=a_agg.pivot(index="week",columns="period",values='num')
    return pivot_table

def get_weekday(date_str):
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        # Get the weekday name
        weekday = date_obj.strftime('%A')
        return weekday
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."


def game_our(our):
    q=""
    for i in our:
        if i=="S":
            q+="B"
        else:
            q+="S"
    our=our[0]+our
    game=2*our[0] + q[:-1] + our[-1]
    return our,game


def prob_table(df, pattern):
    our_ = []
    game_ = []
    prop_ = []
    count_ = []
    round_ = []

    a = create_string(df)
    while len(pattern) > 2:
        our, game = game_our(pattern)
        inv = ""
        if game[-1] == "S":
            inv = "B"
        else:
            inv = "S"
        our_.append(our)
        game_.append(game)
        r1 = count_pattern_occurrences(a, game)
        r2 = count_pattern_occurrences(a, game[:-1] + inv)
        count_.append(r1)
        if (r1==0) & (r2==0):
            return None
        abc = r1 / (r1 + r2)
        prop_.append(round(abc, 2))
        round_.append(len(pattern)-1)
        pattern = pattern[:-1]

    table = {
        'Dot': round_,
        'Our': our_,
        'Game': game_,
        'Count': count_,
        'Probability': prop_
    }
    df = pd.DataFrame(table)
    return df


def popular_patterns(df):
    a=create_string(df)
    haha=[("SSSSSS",count_pattern_occurrences(a,"SSSSSSB")),("BBBBBB",count_pattern_occurrences(a,"BBBBBBS")),
        ("SSBBSS",count_pattern_occurrences(a,"SSBBSSS")),("BBSSBB",count_pattern_occurrences(a,"BBSSBBB")),
        ("SSSBBB",count_pattern_occurrences(a,"SSSBBBB")),("BBBSSS",count_pattern_occurrences(a,"BBBSSSS")),
        ("SBSBSB",count_pattern_occurrences(a,"SBSBSBB")),("BSBSBS",count_pattern_occurrences(a,"BSBSBSS")),
        ("SSBSSB",count_pattern_occurrences(a,"SSBSSBB")),("BBSBBS",count_pattern_occurrences(a,"BBSBBSS"))]
    q1=pd.DataFrame(haha)
    q1[2]=q1.apply(lambda x: round((x[1]/((1440/(len(x[0])+1)) * (df.shape[1]-1)))*100),axis=1)
    q1.loc[10]=['Other',(1440/7 * (df.shape[1]-1))-q1[1].sum(),round(100-q1[2].sum(),2)]
    q1.rename(columns={
        0:"Patterns",
        1:'Counts',
        2:'Percentages'
    },inplace=True)
    return q1


