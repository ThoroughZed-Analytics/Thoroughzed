import requests
from dotenv import load_dotenv
import os
import json
import pandas as pd

load_dotenv()
api_key = os.environ.get('COIN_API_KEY')

url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD/history?period_id=1DAY&time_start=2021-01-01T00%3A00%3A00&time_end=2022-01-01T00%3A00%3A00'
headers = {'X-CoinAPI-Key' : api_key}
response = requests.get(url, headers=headers)

# response_json = response.json()
#
# json_df = pd.read_json(response_json)
#
# print(type(response_json))

# formatted_response = json.dumps(response, indent=4)

# response_json = json.loads(response)

# eth_history_df = pd.DataFrame.from_dict(response_json, orient='columns')
#
# print(formatted_response)