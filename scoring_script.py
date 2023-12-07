import os
import json
import joblib
import numpy as np
import pandas as pd
from azureml.core.model import Model

def init():
    global model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './model_202312071741.pkl')
    model = joblib.load(model_path)

def preprocess(df):
    us_states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]

    def format_phone_no(phone_no):
        phone_no_red = phone_no

        if "x" in phone_no:
            phone_no_red = phone_no.split("x")[0]
        if "+" in phone_no:
            phone_no_red = "".join(phone_no_red.split("-")[1:])

        return phone_no_red \
            .replace("-", "") \
            .replace(".", "") \
            .replace("(", "") \
            .replace(")", "")

    df_trf = df.copy()
    df_trf["mailing_platform"] = df_trf["email"].apply(lambda x: x.split("@")[1])
    df_trf["state"] = df_trf["address"].apply(lambda x: x.split(" ")[-2])
    df_trf["state_valid"] = df_trf["state"].apply(lambda x: 1 if x in us_states else 0)
    df_trf["state"] = df_trf[["state", "state_valid"]].apply(lambda x: x[0] if x[1] else "IV", axis=1)
    df_trf["contact_phone"] = df_trf["contact_phone"].apply(lambda x: format_phone_no(x))
    df_trf["contact_phone_valid"] = df_trf["contact_phone"].apply(lambda x: 1 if len(x) == 10 else 0)
    df_trf["credit_card_no_valid"] = df_trf["credit_card_no"].apply(lambda x: 1 if len(x) == 10 else 0)
    df_trf["birth_month"] = df_trf["date_of_birth"].apply(lambda x: int(x.split("-")[1]))
    df_trf["birth_year"] = df_trf["date_of_birth"].apply(lambda x: int(x.split("-")[0]))
    df_trf["membership_month"] = df_trf["member_since"].apply(lambda x: int(x.split("-")[1]))
    df_trf["membership_year"] = df_trf["member_since"].apply(lambda x: int(x.split("-")[0]))

    return df_trf

def run(raw_data):
    try:
        data = np.array([json.loads(raw_data)["data"]])

        df = pd.DataFrame(data, columns=[
            'address', 'contact_phone', 'credit_card_no', 'customer_name', 'email',
            'id_card_no', 'date_of_birth', 'member_since', 'sex', 'status'
        ])

        df_trf = preprocess(df)
        result = model.predict(df_trf)
        return json.dumps({"result": result.tolist()})
    
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})