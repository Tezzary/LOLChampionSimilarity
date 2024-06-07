import requests
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

api_key = os.getenv("API_KEY")

def params_to_string(params):
    if len(params) == 0:
        return ""
    return "&".join([f"{k}={v}" for k, v in params.items()])

def make_request(endpoint, params={}):
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(endpoint + params_to_string(params), headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()

def safe_make_request(endpoint, params={}):
    while True:
        try:
            return make_request(endpoint, params)
        except Exception as e:
            print(e)
            retry_timer = 5
            print("Retrying... in " + str(retry_timer) + " seconds")
            sleep(retry_timer)