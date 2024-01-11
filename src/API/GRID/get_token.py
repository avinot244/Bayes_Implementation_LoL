import requests
import pandas as pd
import json


def get_token():
    with open("token.json") as f:
        data = json.loads(f.read())
        df = pd.json_normalize(data)
        return df["key"][0]