from flask import Flask
from flask import request
from flask import jsonify

import pandas as pd
import json
import pickle
from training import Preprocessor
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

incidentCodeToTypes  =  {0: 'NetworkIssue', 1: 'NoIssue', 2: 'DatabaseConnection', 3: 'CommunityHealthIssue', 4: 'Community-FromtDoorNotaccessible', 5: 'InvoiceIssue', 6: 'UnsearchableWorkspaces', 7: 'DataLoad Failure'}

# Define model filename
filename = 'model_v3.pk'

@app.route("/predict", methods=['POST'])
def predict_handler():
    
    try:
        req_json = request.get_json()
        
        req_json = str(req_json).replace("'", '"')
        print('Request JSON: \n', req_json)
        
        reqDf = pd.read_json(req_json)
        print('Incoming Request Dataframe: \n', reqDf) 

        
    except Exception as e:
        raise e

    if reqDf.empty :
        return (bad_request())
    else:
        preprocess = Preprocessor()
        
        testX = preprocess.transform(reqDf)
        print('Request test for prediction \n', testX)
        
        print('Request shape = ', str(testX.shape))
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
    
    with open('models/'+filename ,'rb') as f:
        loaded_model = pickle.load(f)
    
    print("The ML model has been loaded and ready for predictions.")
    return loaded_model


model = load_model()

    
app.run(debug=True)