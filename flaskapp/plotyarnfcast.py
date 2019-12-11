import matplotlib
matplotlib.use('Agg')

import pickle
import matplotlib.pyplot as plt
import io
import base64

#predictions = pickle.load(open("yarnpredictions.pkl", 'rb'))
#fcast = pickle.load(open("yarnfcast.pkl", 'rb'))
#error = pickle.load(open("yarnrmse.pkl", 'rb'))
#zData = pickle.load(open("yarnzData.pkl", 'rb'))

def plotyarn(g,predictions,fcast,error,zData):
    title = 'Monthly Global Yarn Usage on Ravelry'
    ylabel='Project Count'
    xlabel=''
    ax = zData[g][0]['Project Count'].plot(legend=True,figsize=(12,6),title=title,fontsize=15, label = 'Historical Data')
    # Does plotting
    #fig= plt.figure()
    fcast[g].plot(legend=True,label='Forecast')
    predictions[g].plot(legend=True,label= 'Validation')
    ax.autoscale(axis='x',tight=True)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    #print(error[g])
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_title(title, fontsize=15)
    #ax.get_legend().remove()
    #plt.show()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(plot_url),error[g]


#y = 'patons-north-america-kroy-socks-fx'
#print(plotyarn(y))