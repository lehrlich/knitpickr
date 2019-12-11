from flaskexample import app
from flask import render_template
from flask import request
import matplotlib.pyplot as plt
import io
import base64
import datetime
from plotyarnfcast import *
# from functions_file import *

predictions = pickle.load(open("yarnpredictions.pkl", 'rb'))
fcast = pickle.load(open("yarnfcast.pkl", 'rb'))
error = pickle.load(open("yarnrmse.pkl", 'rb'))
zData = pickle.load(open("yarnzData.pkl", 'rb'))
trending = pickle.load(open("yarntrending.pkl",'rb'))


#@app.route('/index')
# Home page
@app.route('/')
def index():
    yarn_names = list(predictions.keys())
    plot_url = 'static/select_yarn.png'
    error_output = ''
    return render_template("index.html", yarn_names=yarn_names, plot_url = plot_url, error_output = error_output) 

# "results page"
@app.route('/',methods=['POST'])
def results():
    # Gets input from the dropdown menu
    yarn_selection = request.form['yarn_selection']
    print(yarn_selection)
    
    yarn_names = list(predictions.keys())
    #calculate whether yarn is trending or losing popularity.
    yarn_trend = trending[yarn_selection]
    if yarn_trend>0:
        yarn_statement = 'This yarn is increasing in popularity. Consider stocking.'
        statement_color = 'green'
    else:
        yarn_statement = 'This yarn is losing popularity. Consider decreasing stock.'
        statement_color = 'red'


    plot_url, error_output = plotyarn(yarn_selection,predictions,fcast,error,zData)
    return render_template("index.html", yarn_names=yarn_names, plot_url = plot_url, error_output = error_output, yarn_trend = yarn_trend, yarn_statement=yarn_statement, yarn_selection=yarn_selection, statement_color = statement_color) 

# add new views

months = [
'January',
'February',
'March',
'April',
'May',
'June',
'July',
'August',
'September',
'October',
'November',
'December',
]

@app.route('/input', methods=['GET', 'POST'])
def forLili():
    myDateString = datetime.datetime.today().strftime('%b %d %Y')
    currentMonth = datetime.datetime.today().month

    MONTHS = {}
    for i in range(1, 5):
        MONTHS['plus'+str(i)] = months[(int(currentMonth-1) + i)%12]

    if request.method == 'POST':
        OUTPUT = request.form['month']
        return render_template("input.html", DATE=myDateString, OUTPUT=OUTPUT, MONTHS=MONTHS)
    else:
        return render_template("input.html", DATE=myDateString, OUTPUT='', MONTHS='')

@app.route('/output')
def cesareans_output():
    return render_template("output.html")
