from flask import Flask
from flask import request

import json

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predict_handler():
    input_str = request.form["input"]
    print(input_str)
    input_json = json.loads(input_str)
    print(input_json)
    return predict_impl(input_json)

def predict_impl(input_json):
    # TODO: call actual machine learning predication function here...
    return "todo"

