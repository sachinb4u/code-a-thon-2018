from flask import Flask
from flask import request
from flask import jsonify

import pandas as pd
import json
import pickle
from training import IncidentPreprocessor
import warnings
from sklearn.externals import joblib

warnings.filterwarnings("ignore")

app = Flask(__name__)

incidentCodeToTypes  =  {0: 'NetworkIssue', 1: 'NoIssue', 2: 'DatabaseConnection', 3: 'CommunityHealthIssue', 4: 'Community-FromtDoorNotaccessible', 5: 'InvoiceIssue', 6: 'UnsearchableWorkspaces', 7: 'DataLoad Failure'}



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
        preprocess = IncidentPreprocessor()
        
        # transform request to DF if not Grid model
#         testX = preprocess.transform(reqDf)
#         print('Request test for prediction \n', testX, ' shape = ', str(testX.shape))
        
#         model = load_model()
        
        # pass the req dataframe without transformation as it would hapen in pipeline
        predictions = model.predict(reqDf)
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
    # Define model filename
#     filename1 = 'models/model_random_forest_v1.pk'
#     with open(filename1 ,'rb') as f:
#         loaded_model = pickle.load(f)

    filename2 = 'models/model_xgb_v1.mod'
    loaded_model = joblib.load(filename2)
    
    print("The ML model has been loaded and ready for predictions.")
    return loaded_model


# load the model at startup
model = load_model()

app.run(host='0.0.0.0', debug=True)
