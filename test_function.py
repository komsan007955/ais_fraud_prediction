import requests

url = "https://ais-fraud-prediction.azurewebsites.net/api/predict_ml?code=YmzMTvc1Djd0oOFjSfBVvUpZYIlSlI9yVpksfLVcbWAOAzFujJNQ_g%3D%3D"
data = {
    "address":"9084 Destiny Drives Apt. 873 Cooperton, DC 75097",
    "contact_phone":"0931410005",
    "credit_card_no":"6982000070",
    "customer_name":"Apisit Chaiyachard",
    "email":"5555@example.com",
    "id_card_no":"11027005343335555",
    "date_of_birth":"1995-11-14",
    "member_since":"2021-08-03",
    "sex":"male",
    "status":"single"
}

response = requests.post(url, json=data)

if response.text:
    print(response.text)
else:
    print("Empty response body")