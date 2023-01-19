
from app.model_predict import predict_horse_price
from app.meta_data_query_and_loop_script import get_summary_horse_data
from app.Horse import Horse
import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
import ssl
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from matplotlib.ticker import MaxNLocator
pn.extension('tabulator')

horse_object = get_summary_horse_data(8919)
horse = Horse(horse_object)

market_data_no_outliers = pd.read_csv('https://raw.githubusercontent.com/ThoroughZed-Analytics/Thoroughzed/dev/app/master_db_no_outliers.csv')

abc = market_data_no_outliers.loc[market_data_no_outliers['breed_type'] == horse.breed]
abc = market_data_no_outliers.loc[market_data_no_outliers['bloodline'] == horse.bloodline]

above_average_abc = abc.loc[abc['converted_price'] > abc['converted_price'].mean() + abc['converted_price'].std()]
below_average_abc = abc.loc[abc['converted_price'] < abc['converted_price'].mean()]

avg_percentile,avg_first,avg_races,avg_winnings,avg_price = 'Average',abc['overall.first'].mean(),abc['overall.races'].mean(),abc['total_paid'].mean(),abc['converted_price'].mean()
above_avg_percentile,above_avg_first,above_avg_races,above_avg_winnings,above_avg_price ='Above Average', above_average_abc['overall.first'].mean(),above_average_abc['overall.races'].mean(),above_average_abc['total_paid'].mean(),above_average_abc['converted_price'].mean()
below_avg_percentile,below_avg_first,below_avg_races,below_avg_winnings,below_avg_price = 'Below Average',below_average_abc['overall.first'].mean(),below_average_abc['overall.races'].mean(),below_average_abc['total_paid'].mean(),below_average_abc['converted_price'].mean()
data = [[avg_percentile,avg_first, avg_races, avg_winnings, avg_price],[above_avg_percentile,above_avg_first,above_avg_races,above_avg_winnings,above_avg_price],[below_avg_percentile,below_avg_first,below_avg_races,below_avg_winnings,below_avg_price]]
xyz = pd.DataFrame(data,columns=['Percentile','Number of Wins','Number of Races', 'Amount Won', 'Price'])


# print(len(abc))
# print(len(new_abc))
# print(len(below_average_abc))
# print(abc['converted_price'].std())
# print(abc['converted_price'].mean())
print(xyz)
# print(market_data_no_outliers.columns)
