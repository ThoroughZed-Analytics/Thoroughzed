import requests
from dotenv import load_dotenv
import os
import json
import pandas as pd
import datetime as dt

load_dotenv()
api_key = os.environ.get('COIN_API_KEY')

url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD/history?period_id=1HRS&time_start=2021-01-01T00%3A00%3A00&time_end=2022-01-01T00%3A00%3A00'
headers = {'X-CoinAPI-Key': api_key}
response = requests.get(url, headers=headers)


# convert response data to json and then into pandas df
response_json = response.json()
response_json = json.dumps(response_json)
eth_history_df = pd.read_json(response_json)

# drop unwanted columns (query time period start and stop)
eth_history_df = eth_history_df.drop(['time_period_start', 'time_period_end'], axis=1)

print(eth_history_df.head())

# convert time_open and time_close columns to unix time
# eth_history_df['time_open'] = pd.to_datetime(eth_history_df['time_open'])
# eth_history_df['time_close'] = pd.to_datetime(eth_history_df['time_close'])
