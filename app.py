# -*- coding: utf-8 -*-
"""
Created on April  16 2021

@author: pattn
"""


# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from flask import Flask, request, render_template
import pickle
import xgboost as xgb
import csv



app = Flask("__name__")



q = ""

@app.route("/")
def loadPage():
	return render_template('home.html', query="")


@app.route("/predict", methods=['POST'])
def predict():
    
    inputQuery1 = request.form['query1']
    model = pickle.load(open("xgb.pkl", "rb"))
    
    
    new_df = pd.read_csv("adfald.csv")
    
    y_pred = model.predict(new_df)
    #probablity = model.predict_proba(new_df)[:,1]
    
    o1 = "The list contains all the predicted outputs"
    o2 = ""
    for i in y_pred:
        o2 = o2+str(i)+"\n"
    
#     if single==1:
#         o1 = "The patient is diagnosed with Breast Cancer"
#         o2 = "Confidence: {}".format(probablity*100)
#     else:
#         o1 = "The patient is not diagnosed with Breast Cancer"
#         o2 = "Confidence: {}".format(probablity*100)
        
    return render_template('home.html', output1=o1, output2=o2, query1 = request.form['query1'])
    
if __name__ == "__main__":
    app.run()

