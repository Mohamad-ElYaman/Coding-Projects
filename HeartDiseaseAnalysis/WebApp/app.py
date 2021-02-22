import os
import io
import numpy as np
from flask import Flask, render_template, request, redirect, escape
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions
import requests


# Initialise Flask
app = Flask(__name__)

def getData(request):
    req = request.form
    gender = req['gender']
    age = req['age']
    num_smoke = req['num_smoke']
    stroke = req['stroke']
    sysBP = req['sysBP']
    gluc = req['gluc']
    data = [int(gender), int(age), int(num_smoke), int(stroke), float(sysBP), float(gluc)]
    return(data)

def callApi(data):
    send = {'instances':[]}
    send['instances'] = data
    url = "https://us-east1-heartdisease-297903.cloudfunctions.net/heart-disease"
    reply = requests.post(url, json=send)
    return reply.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=["GET", "POST"])
def predict():
    response = ""
    if request.method == "POST":
        data = getData(request)
        get_reply = callApi(data)
        reply = get_reply[16]
        if reply == '1':
            response = "It is likely that you will develop heart disease in 10 years"
        else:
            response = "It is unlikely that you will develop heart disease in 10 years"
    return render_template("predict.html", result=response)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
