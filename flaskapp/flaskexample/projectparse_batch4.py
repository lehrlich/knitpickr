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
from statsmodels.tools.eval_measures import rmse
from pmdarima import auto_arima                              # for determining ARIMA orders

# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")



def yarncast():
    zData,_= yarnprep()
    predictions={}
    fcast={}
    error={}
    for g in zData:
        split = len(zData[g][0])
        try:
            train = zData[g][0].iloc[:(round(3*split/4))]
            test = zData[g][0].iloc[(round(3*split/4)):]
            #print(zData[g][2])
            model = SARIMAX(train['Project Count'],order=zData[g][1],seasonal_order=zData[g][2])
            results = model.fit()
        except:
            train = zData[g][0].iloc[:(round(11*split/12))]
            test = zData[g][0].iloc[(round(11*split/12)):]
            #print(zData[g][2])
            model = SARIMAX(train['Project Count'],order=zData[g][1],seasonal_order=zData[g][2])
            results = model.fit()
        start=len(train)
        end=len(train)+len(test)-1
        predictions[g] = results.predict(start=start, end=end, dynamic=False, typ='levels').rename('SARIMA(0,1,3)(1,0,1,12) Predictions')
        results = model.fit()
        fcast[g] = results.predict(len(zData[g][0]),len(zData[g][0])+11,typ='levels').rename('SARIMA(0,1,3)(1,0,1,12) Forecast')
        error[g] = rmse(test['Project Count'], predictions[g])
    return predictions,fcast,error,zData
    

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
    #zData = {}
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
        try:
            slicedf2 = cleandf2
            result = seasonal_decompose(slicedf2['Project Count'], model='add')
        except:
            slicedf2 = cleandf2['2017-01-01':'2019-08-01']
            result = seasonal_decompose(slicedf2['Project Count'], model='add')
        decomp[yname]= result
        yData[yname]=slicedf2
    zData=yData
    for k,v in zData.items():
        try:
            aa=auto_arima(v,seasonal=True,m=12)
        except:
            aa = auto_arima(v,seasonal=True)
        zData[k] = (v,aa.order,aa.seasonal_order)
    return zData,decomp

    

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

# myData = yarnprep()
# print(myData)

predictions,fcast,error,zData=yarncast()
f = open("yarnpredictions.pkl","wb")
pickle.dump(predictions,f)
f.close()

f = open("yarnfcast.pkl","wb")
pickle.dump(fcast,f)
f.close()

f = open("yarnrmse.pkl","wb")
pickle.dump(error,f)
f.close()

f = open("yarnzData.pkl","wb")
pickle.dump(zData,f)
f.close()





#myData2 = yarncast()
#print(myData2)
# f = open("yarntimeseries.pkl","wb")
# pickle.dump(myData,f)
# f.close()
