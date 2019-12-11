import pandas as pd
import os 
import re
from bs4 import BeautifulSoup
import csv
from collections import Counter
import pickle
import glob
from pprint import pprint



# def yarncast():
#     yData ={}
#     for yname in myData:
#         df1 =pd.DataFrame(myData[yname][1:-1])
#         df2 = df1.reset_index()
#         df2 = df2.rename(columns={'index':'Date'})
#         df2['Date'] = df2['Date'].apply(pd.to_datetime)
#         df2.set_index('Date',inplace=True)
#         df2.index.freq = '-1MS'
#         df2=df2.sort_index()
#         yData[yname]=df2
#     return df2
    

def processPickle(thisPickle):
    # turn my pickle into a time series
    mynewcounter = Counter()
    for s in thisPickle:
        cleaned_s = re.sub('[IHF].*?  ', '', s)
        mynewcounter[cleaned_s] += 1
    #mynewcounter = Counter([re.sub('[IHF].*?  ', '', s) for s in thisPickle])
    newcounter2 = mynewcounter.copy()
    for key in newcounter2:
        if re.search(r'20[2-9][0-9]|^[IHF]', key):
            del newcounter2[key]
    df=pd.DataFrame.from_dict(newcounter2, orient='index')

    df.columns = ['Project Count']
    x1=df.index
    y1=df['Project Count']
    return df

def projectparse():
    myData = {}
    for fname in glob.glob('flaskexample/static/yarninfo/*.pkl'):
        try:
            thisPickle = pickle.load(open(fname, 'rb'))
            thisdf = processPickle(thisPickle)
            myData[fname.replace('_500.pkl','').replace('flaskexample/static/yarninfo/','')] = thisdf
        except:
            print(fname)
            exit()
    return myData



projectparse()
myData = projectparse()
#myData2 = yarncast()
#print(myData2)
f = open("yarntimeseries.pkl","wb")
pickle.dump(myData,f)
f.close()
