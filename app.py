from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WjEg_NRCYy1apuz3yxqIS4TsuMWJzq3r0WsPkfwlUkXo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("MLToken: " + mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
model = pickle.load(open('employee_prediction.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("AttritionPredictor.html")

@app.route('/predict', methods = ["POST", "GET"])
def predict():
    if request.method == "POST":
        SatisfactionLevel = request.form["SatisfactionLevel"]
        LastEval = request.form["LastEval"]
        NoOfProjects = request.form["NoOfProjects"]
        AverageMonthlyHours = request.form["AverageMonthlyHours"]
        TimeSpentwithCompany = request.form["TimeSpentwithCompany"]
        WorkAccidents = request.form["WorkAccidents"]
        Promotion = request.form["Promotion"]
        Department = request.form["Department"]
        Salary = request.form["Salary"]

        """data = [SatisfactionLevel, LastEval, NoOfProjects, AverageMonthlyHours, TimeSpentwithCompany, WorkAccidents, Promotion, Department, Salary]
        data = [np.array(data)]
        pred = model.predict(data)
        output = pred[0]
        print(output)
        if output == 0:
            return render_template('NegativeOutcome.html')
        else:
            return render_template('PositiveOutcome.html')"""

        payload_scoring = {"input_data": [{"field": ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years', 'Department', 'salary'],
                            "values": [[SatisfactionLevel, LastEval, NoOfProjects, AverageMonthlyHours, TimeSpentwithCompany, WorkAccidents, Promotion, Department, Salary]]}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c9ef2030-5822-4eb2-9762-3407c8d0a838/predictions?version=2021-07-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")

        predictions = response_scoring.json()
        print(predictions['predictions'][0]['values'][0][0])

        if predictions['predictions'][0]['values'][0][0] == 0:
            print("Employee will not leave the company.")
            return render_template('NegativeOutcome.html')
        else:
            print("Employee will leave the company.")
            return render_template('PositiveOutcome.html')

if __name__ == "__main__":
    app.run(debug = True)
