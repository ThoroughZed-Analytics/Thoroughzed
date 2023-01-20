from app.model_predict import predict_horse_price
from app.meta_data_query_and_loop_script import get_summary_horse_data
from app.get_intrinsic_value import get_intrinsic_value, get_intrinsic_value_no_api
from app.model_predict import predict_horse_price
from app.Horse import Horse
import pandas as pd
import numpy as np
import panel as pn
from panel.interact import interact
import holoviews as hv
import hvplot.pandas
import ssl
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from matplotlib.ticker import MaxNLocator
pn.extension('tabulator')
from bokeh.models import DatetimeTickFormatter


def launch_dashboard(id):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # GET HORSE DATA FROM API

    horse_object = get_summary_horse_data(id)
    horse = Horse(horse_object)

    ###############################################################################

    # IMPORT AND CLEAN DATABASES

    # clean_market_data = pd.read_csv('https://raw.githubusercontent.com/ThoroughZed-Analytics/Thoroughzed/dev/app/master_db_no_outliers.csv')
    # clean_market_data = clean_market_data[~pd.isna(clean_market_data['converted_price'])]
    market_data_no_outliers = pd.read_csv('https://raw.githubusercontent.com/ThoroughZed-Analytics/Thoroughzed/dev/app/master_db_no_outliers.csv')

    by_breed = market_data_no_outliers.groupby('breed_type').mean().reset_index()
    breed_daily = market_data_no_outliers.groupby(['day_sold', 'breed_type']).mean().reset_index()
    pd.to_datetime(breed_daily['day_sold'])
    by_blood = market_data_no_outliers.groupby('bloodline').median().reset_index()
    daily = market_data_no_outliers.groupby(['day_sold', 'bloodline']).mean()

    ################################################################################

    # SIDEBAR DATA

    corrected_breed = horse.breed.capitalize()
    if horse.total_races != 0:
        intrinsic_value_lookup_result = get_intrinsic_value(int(horse.horse_id), 1)
        horse_expected_winnings_per_race = f"${intrinsic_value_lookup_result[0]}"
        relative_value = f"${predict_horse_price(int(horse.horse_id))}"

    sidebar_horse_data_message = f"""
        # **{horse.name}**
        ## ***{horse.genotype}*** ***{horse.bloodline}*** ***{corrected_breed}***
        """

    slider_message = " #### **Bid Price in USD:**"

    @interact(Bid=(1, 10000))
    def slider(Price):
        if horse.total_races != 0:
            races = get_intrinsic_value_no_api(Price, horse)[2]
            yield_data = get_intrinsic_value_no_api(Price, horse)[1]
            result = f"""
            ### Financial Summary
            * **Total Winnings:** {"{0:.4f}".format(horse.total_winnings)} ETH 
            * **ZEDstimate:** {relative_value}
            * **Expected Net Winnings / Race:** {horse_expected_winnings_per_race}
            * **Potential 3-Month Yield:** {yield_data}%
            * **Races to Cover Bid Price:** {"{0:,}".format(races)}
            ### Racing Stats
            * **Total Races:** {"{0:,}".format(horse.total_races)}
            * **Win Rate:** {"{0:.2f}".format(horse.win_rate)}%
                * **Free Win Rate:** {"{0:.2f}".format(horse.free_win_rate)}%
                * **Paid Win Rate:** {"{0:.2f}".format(horse.paid_win_rate)}%
            * **Place Rate:** {"{0:.2f}".format(horse.place_rate)}%
            * **Show Rate:** {"{0:.2f}".format(horse.show_rate)}%
            """
            return result
        else:
            return f"""
            ### Financial Summary
            * **Total Winnings:** 0 ETH 
            * **Expected Market Value:** N/A
            * **Expected Net Winnings / Race:** N/A
            * **Potential 3-Month Yield:** N/A
            * **Races to Cover Listing Price:** N/A
            ### Racing Stats
            * **Total Races:** {"{0:,}".format(horse.total_races)}
            * **Win Rate:** {"{0:.2f}".format(horse.win_rate)}%
                * **Free Win Rate:** {"{0:.2f}".format(horse.free_win_rate)}%
                * **Paid Win Rate:** {"{0:.2f}".format(horse.paid_win_rate)}%
            * **Place Rate:** {"{0:.2f}".format(horse.place_rate)}%
            * **Show Rate:** {"{0:.2f}".format(horse.show_rate)}%
            """

    ################################################################################

    # BREED GRAPHS

    def display_df():
        abc = market_data_no_outliers.loc[(market_data_no_outliers['breed_type'] == horse.breed) & (market_data_no_outliers['bloodline'] == horse.bloodline)]
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
        xyz.style.set_properties(**{'text-align': 'right'})

        df_widget = pn.widgets.DataFrame(xyz, name="Stats",show_index=False, width=900)
        return df_widget

    def win_rate_by_breed():
        fig = plt.figure()
        sns.barplot(data=by_breed, x='breed_type', y='win_rate', order=['genesis','legendary', 'exclusive', 'elite', 'cross', 'pacer'])
        plt.xlabel('Breed')
        plt.ylabel('Win Rate (%)')
        plt.title('Mean Win Rate by Breed')
        return fig

    def hv_line_breed():
        breed_daily['day_sold'] = pd.to_datetime(breed_daily['day_sold'])
        xformatter = DatetimeTickFormatter(days="%Y-%m-%d")
        list_of_plots = [hv.Curve(breed_daily.loc[breed_daily['breed_type']=='genesis'][['day_sold', 'converted_price']], label='Genesis'),
            hv.Curve(breed_daily.loc[breed_daily['breed_type']=='legendary'][['day_sold', 'converted_price']], label='Legendary'),
            hv.Curve(breed_daily.loc[breed_daily['breed_type']=='exclusive'][['day_sold', 'converted_price']], label='Exclusive'),
            hv.Curve(breed_daily.loc[breed_daily['breed_type']=='elite'][['day_sold', 'converted_price']], label='Elite'),
            hv.Curve(breed_daily.loc[breed_daily['breed_type']=='cross'][['day_sold', 'converted_price']], label='Cross'),
            hv.Curve(breed_daily.loc[breed_daily['breed_type']=='pacer'][['day_sold', 'converted_price']], label='Pacer')]
        return hv.Overlay(list_of_plots).opts(xlabel='Date', ylabel='Sale Price (USD)',title='Sale Price by Breed Over Time', legend_position='right',width=1000, height=500,xformatter=xformatter, xticks=10, xrotation=30,active_tools=['box_zoom'])

    def line_breed():
        fig, ax = plt.subplots()
        sns.lineplot(data=breed_daily, x='day_sold', y='converted_price', hue='breed_type', hue_order=['genesis', 'legendary', 'exclusive', 'elite', 'cross', 'pacer'])
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
        plt.xticks(rotation=20)
        plt.xlabel('Date')
        plt.ylabel('Sale Price (USD)')
        plt.title('Sale Price by Breed Over Time')
        handles, labels = ax.get_legend_handles_labels()
        for handle in handles:
            handle.set_linewidth(2.0)
            handle.set_linestyle("-")
        plt.legend(title='Breed', handles=handles, labels=['Genesis', 'Legendary', 'Exclusive', 'Elite', 'Cross', 'Pacer'])
        fig.set_size_inches(13,6)
        return fig

    ##############################################################################

    # BLOODLINE GRAPHS

    def barchart_median_win_by_blood():
        fig = plt.figure()
        sns.barplot(data=by_blood, x='bloodline', y='win_rate', order=['Nakamoto', 'Szabo', 'Finney', 'Buterin'])
        plt.xlabel('Bloodline')
        plt.ylabel('Win Rate (%)')
        plt.title('Mean Win Rate by Bloodline')
        return fig

    def avg_win_by_bloodline():
        fig = plt.figure()
        sns.barplot(data=by_blood, x='bloodline', y='overall.first', order=['Nakamoto', 'Szabo', 'Finney', 'Buterin'])
        plt.xlabel('Bloodline')
        plt.ylabel('Mean Number of Wins')
        plt.title('Mean Number of Wins by Bloodline')
        return fig

    def line_blood():
        fig, ax = plt.subplots()
        sns.lineplot(data=daily, x='day_sold', y='converted_price', hue='bloodline', hue_order=['Nakamoto', 'Szabo', 'Finney', 'Buterin'])
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
        plt.xticks(rotation=20)
        plt.xlabel('Date')
        plt.ylabel('Sale Price (USD)')
        plt.title('Sale Price by Bloodline Over Time')
        plt.legend(title='Bloodline', labels=['Nakamoto', 'Szabo', 'Finney', 'Buterin'])
        colors = ['blue', 'orange', 'green', 'red']
        count = 0
        leg = ax.get_legend()
        handles, labels = ax.get_legend_handles_labels()
        for handle in handles:
            handle.set_linewidth(2.0)
            handle.set_linestyle("-")
            leg.legendHandles[count].set_color(colors[count])
        plt.legend(title='Bloodline', handles=handles, labels=labels)
        fig.set_size_inches(13,6)
        return fig

    ###############################################################################

    # DASHBOARD RENDERING

    template = pn.template.FastListTemplate(
        title='ThoroughZED Analytics', logo='https://i.imgur.com/3rpZHfT.png', header_background='#09a59f', header_color='black', font='times', shadow=True, corner_radius=20, favicon='https://i.imgur.com/3rpZHfT.png', theme_toggle=False, busy_indicator=None,
        sidebar=[pn.pane.Markdown(sidebar_horse_data_message),
                 pn.pane.Markdown(slider_message),
                 pn.Column(slider),
                 pn.pane.PNG(horse.img_url, sizing_mode='scale_both')],
        main=[pn.Row(pn.Column(display_df)),
              pn.Row(pn.Column(hv_line_breed),
                     pn.Column(win_rate_by_breed)),
              pn.Row(pn.Column(line_blood),
                     pn.Column(avg_win_by_bloodline))],
        accent_base_color="#88d8b0",
    )
    template.show()


if __name__ == "__main__":
    launch_dashboard(8919)
