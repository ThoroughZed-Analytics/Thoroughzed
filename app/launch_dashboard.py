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
    breed_daily = market_data_no_outliers.groupby(['day_sold', 'breed_type']).mean()
    by_blood = market_data_no_outliers.groupby('bloodline').median().reset_index()
    daily = market_data_no_outliers.groupby(['day_sold', 'bloodline']).mean()

    ################################################################################

    # BREED GRAPHS

    def rate_by_breed():
        plot = sns.barplot(data=by_breed, x='breed_type', y='win_rate')
        return plot.figure

    barchart_win_rate_by_breed = sns.barplot(data=by_breed, x='breed_type', y='win_rate')
    # barchart_win_rate_by_breed = barchart_win_rate_by_breed.plt.title('Mean Win Rate by Breed Type')

    barchart_avg_win_num_by_breed = sns.barplot(data=by_breed, x='breed_type', y='overall.first')
    # barchart_avg_win_num_by_breed = barchart_avg_win_num_by_breed.plt.title('Mean Number of 1st Place Finishes by Breed')

    violin_usd_price_by_breed = sns.violinplot(data=market_data_no_outliers, x='breed_type', y='converted_price')

    lineplot_sale_price_breed_time = sns.lineplot(data=breed_daily, x='day_sold', y='converted_price', hue='breed_type')
    # lineplot_sale_price_breed_time = lineplot_sale_price_breed_time.plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    # lineplot_sale_price_breed_time = lineplot_sale_price_breed_time.plt.xticks(rotation=45)
    # lineplot_sale_price_breed_time = lineplot_sale_price_breed_time.set(xlabel=None)
    # lineplot_sale_price_breed_time = lineplot_sale_price_breed_time.plt.ylabel('Sale Price (USD)')
    # lineplot_sale_price_breed_time = lineplot_sale_price_breed_time.plt.title('Horse Sale Price by Breed Over Time')

    ##############################################################################

    # BLOODLINE GRAPHS

    barchart_median_win_by_blood = sns.barplot(data=by_blood, x='bloodline', y='win_rate')
    # barchart_median_win_by_blood = barchart_median_win_by_blood.plt.title('Median Win Rate by Bloodline')
    # barchart_median_win_by_blood = barchart_median_win_by_blood.plt.xticks(rotation=45)

    lineplot_sale_price_blood_time = sns.lineplot(data=daily, x='day_sold', y='converted_price', hue='bloodline')
    # lineplot_sale_price_blood_time = lineplot_sale_price_blood_time.plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    # lineplot_sale_price_blood_time = lineplot_sale_price_blood_time.plt.xticks(rotation=45)
    # lineplot_sale_price_blood_time = lineplot_sale_price_blood_time.set(xlabel=None)
    # lineplot_sale_price_blood_time = lineplot_sale_price_blood_time.plt.ylabel('Sale Price (USD)')
    # lineplot_sale_price_blood_time = lineplot_sale_price_blood_time.plt.title('Horse Sale Price by Bloodline Over Time')

    ###############################################################################

    # DASHBOARD RENDERING

    template = pn.template.FastListTemplate(
        title='ThoroughZED Analytics - Relative Valuation', logo='https://i.imgur.com/3rpZHfT.png', header_background='black', header_color='red', font='times', shadow=True,
        sidebar=[pn.pane.Markdown("## Horse Data"),
                 pn.pane.Markdown(
                     "#### Carbon dioxide emissions are the primary driver of global climate change. It’s widely recognised that to avoid the worst impacts of climate change, the world needs to urgently reduce emissions. But, how this responsibility is shared between regions, countries, and individuals has been an endless point of contention in international discussions."),
                 pn.pane.PNG(horse.img_url, sizing_mode='scale_both'),
                 pn.pane.Markdown("## Settings")],
        main=[pn.Row(pn.Column(rate_by_breed),
                     barchart_avg_win_num_by_breed)],
        accent_base_color="#88d8b0",
    )
    template.show()

    # ACCENT_COLOR = pn.template.FastGridTemplate.accent_base_color
    # XS = np.linspace(0, np.pi)
    #
    # def sine(freq, phase):
    #     return hv.Curve((XS, np.sin(XS * freq + phase))).opts(
    #         responsive=True, min_height=400, title="Sine", color=ACCENT_COLOR
    #     ).opts(line_width=6)
    #
    # def cosine(freq, phase):
    #     return hv.Curve((XS, np.cos(XS * freq + phase))).opts(
    #         responsive=True, min_height=400, title="Cosine", color=ACCENT_COLOR
    #     ).opts(line_width=6)
    #
    # freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
    # phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)
    #
    # sine = pn.bind(sine, freq=freq, phase=phase)
    # cosine = pn.bind(cosine, freq=freq, phase=phase)
    #
    # template = pn.template.FastGridTemplate(
    #     site="ThoroughZED Analytics", title="Relative Valuation Dashboard",
    #     header_color='red', header_background='black', theme='dark',
    #     main_layout='card',
    #     sidebar=[pn.pane.Markdown("## Settings"), freq, phase],
    # )
    #
    # template.main[:3, :6] = pn.pane.HoloViews(hv.DynamicMap(sine), sizing_mode="stretch_both")
    # template.main[:3, 6:] = pn.pane.HoloViews(hv.DynamicMap(cosine), sizing_mode="stretch_both")
    # template.show()


if __name__ == "__main__":
    launch_dashboard(8919)
