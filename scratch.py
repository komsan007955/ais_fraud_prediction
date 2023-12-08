import requests

def test_azure_function():
    #url = "https://fraudpremium1.azurewebsites.net/api/http_trigger"
    url = "http://localhost:7071/api/Trigger101"
    # headers = {
    #     'x-functions-key': 'bHFGAY9SG-6A-fJ1FaQVLTKdpNMXYsT5RuODCqEALtWBAzFuC3bZQw==',  # If needed
    #     'Content-Type': 'application/json'
    # }

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'name': '0662485036'
    }

    response = requests.post(url, json=data, headers=headers)
     
     # ... your code to get the response ...
    if response.text:
        print(response.text)
    else:
        print("Empty response body")
    assert response.status_code == 200


# Run the test
test_azure_function()