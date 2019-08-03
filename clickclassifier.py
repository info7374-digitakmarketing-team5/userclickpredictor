#import libraries
from flask import Flask,render_template,url_for,request
import pickle
from sklearn.externals import joblib
import urllib.request
import json
import datetime

#function to classify user's click based on their demographic details
def click_classifier(daily_time_spent, age, income, daily_internet_usage, male, month, day_month, weekday):
    classify_model = open('./classify_cust_click1.pkl','rb')
    clk = joblib.load(classify_model)
    click_prediction = ''
    click_prediction = clk.predict([[daily_internet_usage, age, income, daily_internet_usage, male, month, day_month, weekday]])
    return click_prediction[0]

def azure_classifier(daily_time_spent, age, income, daily_internet_usage, male, date_clicked_ts):
    data = {
        "Inputs":{
            "input1":[
                {
                    'Daily Time Spent on Site': daily_time_spent,   
                    'Age': age,   
                    'Area Income': income,   
                    'Daily Internet Usage': daily_internet_usage,   
                    'Ad Topic Line': "Cloned 5thgeneration orchestration",   
                    'City': "Wrightburgh",   
                    'Male': male,   
                    'Country': "Tunisia",   
                    'Timestamp': date_clicked_ts,   
                    'Clicked on Ad': "0",   
                }
            ],
        },
        "GlobalParameters":{

        }
    }

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    body = str.encode(json.dumps(data, default = myconverter))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/ef38c30a218d4b6596c184f8980f563f/services/b306c2c378f64c0b83be8c8de8bf064b/execute?api-version=2.0&format=swagger'
    api_key = 'kF0DpKj2wPUB6ytds1+59ejPqrq8qWQyajN/0MhqrYUx5sSm+toveiz6SzfEI91Ax/K4QxLm++NdEbCjQ+Ga9w==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    
    req = urllib.request.Request(url, body, headers)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    print (result)
    d = json.loads(result)
    print (d['Results']['output1'][0]['Scored Labels'])
    return d['Results']['output1'][0]['Scored Labels']