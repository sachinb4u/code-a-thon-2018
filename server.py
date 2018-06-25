from flask import Flask
from flask import request
from flask import jsonify

import pandas as pd
import json
import pickle

app = Flask(__name__)

incidentLabels = ['NoIssue', 'DBConnectionIssue', 'InvoiceIssue', 'OrderIssue', 'CommunityIssue',
                 'WorkspaceIssue' , 'NetworkIssue', 'CommunityHealthIssue' ]

filename = 'model_v1.pk'

@app.route("/predict", methods=['POST'])
def predict_handler():
    
    try:
        req_json = request.get_json()
        print('Request JSON = \n', req_json)
        req_json = str(req_json).replace("'", '"')
        print('Request JSON Updated= \n', req_json)
        
        reqDf = pd.read_json(req_json)
        
        print(reqDf)
        
    except Exception as e:
        raise e

    if reqDf.empty :
        return (bad_request())
    else:
        #Load the saved model
        model = load_model()
        
        print("The model has been loaded...doing predictions now...")
        
        predictions = model.predict(reqDf)
        predNames = pd.Series(predicitons).apply(lambda x : incidentTypes[x])
        
        responses = jsonify(predictions=predNames)
    
    return (responses)

def bad_request():
    bad_response = '{"error" : "bad request"}'
    response1 = jsonify(bad_response)
    response1.status_code = 400
    
    return response1

def load_model():
    model_filename = 'model_v1.pk'
    with open('models/'+filename ,'rb') as f:
        loaded_model = pickle.load(f)
        
    return loaded_model

if __name__ == "__main__" :
    app.run(debug=True)
    
# app.run(debug=True)