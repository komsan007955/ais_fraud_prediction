import azure.functions as func
import logging
import urllib.request

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            """This HTTP triggered function executed successfully. 
                Pass a name in the query string or in the request body 
                for a personalized response.""", \
            status_code=200
        )

@app.route(route="predict_ml")
def predict_ml(req: func.HttpRequest) -> func.HttpResponse:
    url = "https://fraud-prediction.eastus2.inference.ml.azure.com/score"
    headers = {
        "Content-Type": "application/json", 
        "Authorization": ("Bearer qH9VQupVmqZf28PlDVB2cb0FxApCHDlf"), 
        "azureml-model-deployment": "fraud-prediction-1"
    }
    req_api = urllib.request.Request(url, req.get_body(), headers)

    try:
        res_api = urllib.request.urlopen(req_api)
        res = res_api.read()
        return func.HttpResponse(res)
    except urllib.error.HTTPError as error:
        res = f"""
            The request failed with status code: {str(error.code)}\n
            {error.info()}\n
            {error.read().decode("utf8", "ignore")}
        """
        return func.HttpResponse(res)