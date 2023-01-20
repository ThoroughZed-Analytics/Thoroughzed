import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn
import hvplot.pandas
import sklearn
import datetime
from matplotlib.ticker import MaxNLocator
from matplotlib.gridspec import GridSpec
import holoviews as hv
from holoviews import opts
from panel.interact import interact
# import geoviews as gv
hv.extension('bokeh')
# gv.extension('bokeh')



pn.extension('tabulator')

clean_market_data = pd.read_csv('https://raw.githubusercontent.com/ThoroughZed-Analytics/Thoroughzed/dev/app/master_db_no_outliers.csv')
def open_dash():
    # ACCENT_COLOR = pn.template.FastGridTemplate.accent_base_color

    graph1_df = clean_market_data.groupby(['day_sold','breed_type']).mean()
    # print(graph1_df.columns)
    pn.extension()

    def graph1():
        # breeds = list(clean_market_data.breed_type.unique())
        # select = pn.widgets.Select(name="Breeds", options=breeds)
        # def create_plot(breed):
        #     data = clean_market_data.loc[clean_market_data['breed_type'] == breed]
        #     return data.hvplot('day_sold','breed_type')
        # interact(create_plot,symbol=select)
        return clean_market_data.groupby(['day_sold','breed_type']).mean().hvplot('day_sold','breed_type').show()

    graph1()

if __name__ == '__main__':
    open_dash()   
    
    
    
    
             # time_slider = pn.widgets.FloatSlider(name="Time", start=0, end=10, value=2)

            # graph1 = pn.bind(graph1, time=time_slider)
            # graph3 = pn.bind(graph2, time=time_slider)