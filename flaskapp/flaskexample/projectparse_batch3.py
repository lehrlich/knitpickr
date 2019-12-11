import pandas as pd
import os 
import re
from bs4 import BeautifulSoup
import csv
from collections import Counter
import pickle
import glob
from pprint import pprint
import pandas as pd
import numpy as np
#%matplotlib inline

# Load specific forecasting tools
from statsmodels.tsa.statespace.sarimax import SARIMAX

from statsmodels.graphics.tsaplots import plot_acf,plot_pacf # for determining (p,q) orders
from statsmodels.tsa.seasonal import seasonal_decompose      # for ETS Plots
from pmdarima import auto_arima                              # for determining ARIMA orders

# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")


def yarnprep():
    new_dict = projectparse()
    try:
        del new_dict['caron-simply-soft-tweeds-2']
    except KeyError:
        pass
    try:
        del new_dict['red-heart-super-saver-solids']
    except KeyError:
        pass
    try:
        del new_dict['malabrigo-yarn-rios']
    except KeyError:
        pass

    yData ={}
    decomp = {}
    for yname in new_dict:
        df1 =pd.DataFrame(new_dict[yname][1:-1])
        df2 = df1.reset_index()
        df2 = df2.rename(columns={'index':'Date'})
        df2 = df2[df2.Date != 'In progress']
        df2 = df2[df2.Date != 'Hibernating']
        df2 = df2[df2.Date != 'Frogged']
        df2 = df2[df2.Date != 'Finished']
        df2['Date'] = pd.to_datetime(df2['Date'], dayfirst=True, errors='coerce')
        df2= df2.set_index('Date')
        df2=df2.sort_index()
        cleandf2 = df2.dropna()
        slicedf2 = cleandf2['2017-01-01':'2019-08-01']
        result = seasonal_decompose(slicedf2['Project Count'], model='add')
        decomp[yname]= result
        yData[yname]=slicedf2
    return yData,decomp

    

def processPickle(thisPickle):
    # turn my pickle into a time series
    mynewcounter = Counter()
    for s in thisPickle:
        cleaned_s = re.sub('[IHF].*?  ', '', s)
        mynewcounter[cleaned_s] += 1
    #mynewcounter = Counter([re.sub('[IHF].*?  ', '', s) for s in thisPickle])
    newcounter2 = mynewcounter.copy()
    # for key in newcounter2:
    #     if re.search(r'20[2-9][0-9]|^[IHF]', key):
    #         del newcounter2[key]
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



#myData2 = yarncast()
#print(myData2)
# f = open("yarntimeseries.pkl","wb")
# pickle.dump(myData,f)
# f.close()
