# scoring_script.py

import os
import json
import joblib
import numpy as np
from azureml.core.model import Model

def init():
    global model
    # Retrieve the path to the model file using the model name
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './model.pkl')
    # Load the model
    model = joblib.load(model_path)

def run(raw_data):
    try:
        # Convert the raw data to a numpy array
        data = json.loads(raw_data)["data"]
        data = np.array(data)
	
        # Get the data preprocessed
        data_prep = preprocess(data).reshape(1, -1)
        
        # Make predictions
        result = model.predict(data_prep)

        # You can return any JSON-serializable result. Here, we return a list.
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})

def preprocess(data):
    return np.vectorize(np.float32)(np.delete(data, [2, 3]))