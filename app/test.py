
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

price_10p, price_25p, price_50p, price_75p, price_90p = np.percentile(abc['converted_price'], [10, 25, 50, 75, 90])
win_rate_10p, win_rate_25p, win_rate_50p, win_rate_75p, win_rate_90p = np.percentile(abc['win_rate'], [10, 25, 50, 75, 90])
races_10p, races_25p, races_50p, races_75p, races_90p = np.percentile(abc['overall.races'], [10, 25, 50, 75, 90])
totalETH_10p, totalETH_25p, totalETH_50p, totalETH_75p, totalETH_90p = np.percentile(abc['total_paid'], [10, 25, 50, 75, 90])
avg_win_rate,avg_races,avg_winnings,avg_price = abc['win_rate'].mean(),abc['overall.races'].mean(),abc['total_paid'].mean(),abc['converted_price'].mean()

price_list = [price_10p, price_25p, price_50p, price_75p, price_90p]
price_formatted = [f"${'{0:.2f}'.format(x)}" for x in price_list]

win_rate = [win_rate_10p, win_rate_25p, win_rate_50p, win_rate_75p, win_rate_90p]
win_rate_formatted = [f"{'{0:.2f}'.format(x)}%" for x in win_rate]

races_list = [races_10p, races_25p, races_50p, races_75p, races_90p]
races_formatted = [int(x) for x in races_list]

totalETH_list = [totalETH_10p, totalETH_25p, totalETH_50p, totalETH_75p, totalETH_90p]
totalETH_formatted = [f"{'{0:.4f}'.format(x)} ETH" for x in totalETH_list]


ten_p_values = [win_rate_formatted[0], races_formatted[0], totalETH_formatted[0], price_formatted[0]]
twenty_five_p_values = [win_rate_formatted[1], races_formatted[1], totalETH_formatted[1], price_formatted[1]]
median_values = [win_rate_formatted[2], races_formatted[2], totalETH_formatted[2], price_formatted[2]]
seven_five_p_values = [win_rate_formatted[3], races_formatted[3], totalETH_formatted[3], price_formatted[3]]
nine_zero_p_values = [win_rate_formatted[4], races_formatted[4], totalETH_formatted[4], price_formatted[4]]
avg_values = [f"{'{0:.2f}'.format(avg_win_rate)}%", int(avg_races), f"{'{0:.4f}'.format(avg_winnings)} ETH", f"${'{0:.2f}'.format(avg_price)}"]

ten_p_name, twenty_five_p_name, median_name, average_name, seven_five_p_name, nine_zero_p_name = ['10th Percentile', '25th Percentile', 'Median', 'Average', '75th Percentile', '90th Percentile']

data = [[ten_p_name,ten_p_values[0], ten_p_values[1], ten_p_values[2], ten_p_values[3]],[twenty_five_p_name, twenty_five_p_values[0],twenty_five_p_values[1], twenty_five_p_values[2], twenty_five_p_values[3]],[median_name, median_values[0], median_values[1], median_values[2], median_values[3]], [average_name, avg_values[0], avg_values[1], avg_values[2], avg_values[3]], [seven_five_p_name, seven_five_p_values[0], seven_five_p_values[1], seven_five_p_values[2], seven_five_p_values[3]], [nine_zero_p_name, nine_zero_p_values[0], nine_zero_p_values[1], nine_zero_p_values[2], nine_zero_p_values[3]]]
xyz = pd.DataFrame(data,columns=['Percentile','Win Rate','Number of Races', 'Gross Winnings', 'Sale Price'])
breed_daily_df = market_data_no_outliers[['day_sold','breed_type','converted_price']]
# breed_daily = market_data_no_outliers.groupby(['day_sold', 'breed_type'])['test']['test2'].mean()
# breed_daily = market_data_no_outliers[['day_sold', 'breed_type']]
# breed_daily_df = pd.DataFrame({'mean': market_data_no_outliers.groupby(['day_sold', 'breed_type']).mean()}).reset_index()

# print(len(abc))
# print(len(new_abc))
# print(len(below_average_abc))
# print(abc['converted_price'].std())
# print(abc['converted_price'].mean())
# print(breed_daily)
# print(f"{breed_daily['Unnamed: 0.1']}")
# print(breed_daily['Unnamed: 0'])
# print(market_data_no_outliers.columns)
print(breed_daily_df)
# print(market_data_no_outliers.columns)
