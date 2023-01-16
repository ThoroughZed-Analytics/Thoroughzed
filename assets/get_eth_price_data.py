import requests
from dotenv import load_dotenv
import os
import json
import pandas as pd
import datetime as dt

# functions to convert from base time format into unix time in seconds and round down to 2 digits


def make_unix(datetime):
    return ((datetime.tz_convert(None) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')) // 3600


def round_2(price):
    return round(price, 2)


load_dotenv()
api_key = os.environ.get('COIN_API_KEY')

url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD/history?period_id=1HRS&time_start=2021-01-01T00%3A00%3A00&time_end=2022-01-01T00%3A00%3A00'
headers = {'X-CoinAPI-Key' : api_key}

response = requests.get(url, headers= headers)

# convert response data to json and then into pandas df
response_json = response.json()
response_json = json.dumps(response_json)
eth_history_df = pd.read_json(response_json)


# drop unwanted columns (query time period start and stop)
eth_history_df = eth_history_df.drop(['time_period_start', 'time_period_end', 'rate_high', 'rate_low', 'rate_close', 'time_close'], axis=1)

# convert time_open and time_close columns to datetime format
eth_history_df['time_open'] = pd.to_datetime(eth_history_df['time_open'])

# apply unix conversion to time columns and round down price
eth_history_df['time_open'] = eth_history_df['time_open'].apply(make_unix)
eth_history_df['rate_open'] = eth_history_df['rate_open'].apply(round_2)

eth_history_df = eth_history_df.rename(columns={'rate_open': 'eth_price', 'time_open': 'timestamp'})

print(eth_history_df)

eth_history_df.to_csv('eth_price_history.csv')
