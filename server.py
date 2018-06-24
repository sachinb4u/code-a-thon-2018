from flask import Flask
from flask import request

import json
import pickle

app = Flask(__name__)


incidentLabels = ['NoIssue', 'DBConnectionIssue', 'InvoiceIssue', 'OrderIssue', 'CommunityIssue',
                 'WorkspaceIssue' , 'NetworkIssue', 'CommunityHealthIssue' ]

@app.route("/predict", methods=['POST'])
def predict_handler():
    input_str = request.form["input"]
    print(input_str)
    input_json = json.loads(input_str)
    print(input_json)
    return predict_impl(input_json)

def predict_impl(input_json):
    # TODO: call actual machine learning predication function here...
    model = load_model()
    prediction = model.predict()
    
    predictionName = prediciton.apply(lambda x : inidentLabels[x])
    
    return "todo"


def load_model():
    model_filename = 'model_v1.pk'
    with open('models/'+filename ,'rb') as f:
        loaded_model = pickle.load(f)
        
    return loaded_model

