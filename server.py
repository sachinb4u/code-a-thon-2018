from flask import Flask
from flask import request
from flask import jsonify

import pandas as pd
import json
import pickle
from training import Preprocessor

app = Flask(__name__)

incidentLabels = ['NoIssue', 'DBConnectionIssue', 'InvoiceIssue', 'OrderIssue', 'CommunityIssue',
                 'WorkspaceIssue' , 'NetworkIssue', 'CommunityHealthIssue' ]

incidentTypesDict = {'NoIssue' : 0, 'DBConnectionIssue' :1, 'InvoiceIssue' :2, 
                     'OrderIssue' :3,  'CommunityIssue' :4, 'WorkspaceIssue' :5 ,
                     'NetworkIssue' :6, 'CommunityHealthIssue':7 }

incidentCodeToTypes = {0 :'NoIssue' , 1: 'DBConnectionIssue', 2: 'InvoiceIssue', 
                     3: 'OrderIssue', 4: 'CommunityIssue', 5: 'WorkspaceIssue',
                     6: 'NetworkIssue', 7: 'CommunityHealthIssue' }

filename = 'model_v1.pk'
model = None

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
        preprocess = Preprocessor()
        
        testX = preprocess.transform(reqDf)
        print('Request test for prediction \n', testX)
        
        predictions = model.predict(testX)
        print('Prediction = \n' , predictions)
        
        predDf = pd.DataFrame(data=predictions, columns=['code'])        
        predDf['name'] = predDf['code'].replace(to_replace=incidentCodeToTypes)
        
        print('PredictionDF = \n' , predDf)

        jsonResp = predDf.to_json(orient='records')
        print('Prediction result = ', jsonResp)
        
        responses = jsonResp
    
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
    # load model at startup
    model = load_model()
    print("The ML model has been loaded and ready for predictions.")
    app.run(debug=True)
    
# app.run(debug=True)