import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WjEg_NRCYy1apuz3yxqIS4TsuMWJzq3r0WsPkfwlUkXo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years', 'Department', 'salary'],
                    "values": [[0.84, 0.92, 4, 234, 5, 0, 0, 6, 1]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c9ef2030-5822-4eb2-9762-3407c8d0a838/predictions?version=2021-07-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")

predictions = response_scoring.json()
print(predictions['predictions'][0]['values'][0][0])

if predictions == 0:
    print("Employee will not leave the company.")
else:
    print("Employee will leave the company.")
