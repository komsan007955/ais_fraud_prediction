import json
import numpy as np
import pickle

def init():
    global model
    # Load the model
    model = pickle.load(open("azure_test/model/model.pkl", "rb"))

def run(raw_data):
    try:
        # Convert the raw data to a numpy array
        data = raw_data["data"]
        data = np.array(data)
	
        # Get the data preprocessed
        data_prep = preprocess(data).reshape(1, -1)
        
        # Make predictions
        result = model.predict(data_prep)

        # You can return any JSON-serializable result. Here, we return a list.
        print(json.dumps({"result": result.tolist()}))
    except Exception as e:
        error = str(e)
        print(json.dumps({"error": error}))

def preprocess(data):
    return np.vectorize(np.float32)(np.delete(data, [2, 3]))

init()
run({"data": [8937,44551,"2005-12-23",4.0,2,173538]})