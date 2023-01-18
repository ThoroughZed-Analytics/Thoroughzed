from app.get_intrinsic_value import get_intrinsic_value
from termcolor import colored
from assets.art import art
from app.get_relative_value import get_relative_value
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from json import load
import ssl
import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
pn.extension('tabulator')

import hvplot.pandas
import panel.template.theme


def help():
    print("""
    How to Value a ZED Run Racehorse
    
    There are two ways to value a horse:
    1. Intrinsic Valuation
        - This model is based on how much money the horse is generating racing
        - The model will evaluate the provided horse id and listing price and provide the following:
            1. Expected Net Earnings / Race
            2. Expected 3-Month Yield
            3. Number of Races to Recoup the Cost of the Horse
        - For a more detailed explanation, please visit our Medium post here: https://tinyurl.com/how-to-value-ZED
    2. Relative Valuation
        - This model is based on comparable sales in the marketplace
        - The model will evaluate the provided horse id and take you to a dashboard to explore all sales of comparable horses
        - You will be able to see the the breakout of prices paid for similar horses
        - As a rule of thumb, you should not be will to pay more for a horse than the percentile of its win percentage
        - EX: If a horse has a 60th percentile win rate, you should not be willing to pay the 80th percentile price
    
    NOTE: This model is a decision-making tool to assist in the evaluation of a given listing price or a bid you expect to put on a horse.
        It is to be used to gauge the feasibility of making your money back on your investment given the price of the horse, however, this
        does not constitute financial advice nor guarantee the performance of the horse.
    """)


def run_cli():
    color_words = [colored('Horse/NFT ID', 'green', attrs=['bold']), colored("'q'", 'red', attrs=['bold']),
                   colored("> *** Not a valid ID! ***",'red', attrs=['blink']),
                   colored('(r)elative value', 'green'), colored('(i)ntrinsic value', 'green')]
    print(colored(art, 'green', attrs=['blink']))
    id = input(f"> Please enter the {color_words[0]} for the horse you'd like to evaluate or type {color_words[1]} to quit. Or h for help. ")
    if id.lower() == "q":
        exit()
    while id.lower() == 'h':
        help()
        id = input(f"> Please enter the Horse/NFT ID for the horse you'd like to evaluate or type {color_words[1]} to quit. Or h for help. ")
        if id.lower() == "q":
            exit()
    while not id.isdigit():
        print(f"{color_words[2]}")
        id = input(f"> Please enter the Horse/NFT ID for the horse you'd like to evaluate or type {color_words[1]} to quit. Or h for help. ")
        if id.lower() == "q":
            exit()
    choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit. Or h for help. ")
    if choice.lower() == 'h':
        help()
    if choice.lower() == "q":
        exit()
    while choice != "r" and choice != "i":
        print(f"{color_words[2]}")
        choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit. Or h for help.")
        if id.lower() == "q":
            exit()
    if choice == "i":
        cost = input(f"> Enter the listing price of the horse in USD. Or type {color_words[1]} to quit. ")
        if cost.lower() == "q":
            exit()
        while not cost.isdigit():
            print("> *** Not a valid cost! ***")
            cost = input(f"> Enter the listing price of the horse in USD. Or type {color_words[1]} to quit. ")
            if cost.lower() == "q":
                exit()
        results = get_intrinsic_value(int(id), int(cost))
        if type(results) == str:
            print('Cannot conduct intrinsic valuation because the horse is unraced.') 
        else:
            if float(results[0]) >= 0:
                print('> Potential Net Earnings Per Race: ', colored(f'${results[0]}', 'green'))
            else:
                print('> Potential Net Earnings Per Race: ', colored(f'${results[0]}', 'red'))
            if float(results[1]) >= 0:
                print('> Potential 3-Month Yield: ', colored(f'{results[1]}%', 'green'))
            else:
                print('> Potential 3-Month Yield: ', colored(f'{results[1]}%', 'red'))
            if float(results[2]) >= 0:
                print('> Races Needed to Cover Cost of Horse: ', colored(f'{"{0:,}".format(results[2])}', 'green'))
            else:
                print('> Races Needed to Cover Cost of Horse: ', colored(f'{"{0:,}".format(results[2])}', 'red'))

    if choice == "r":
        num = get_relative_value(int(id))
        print(num)

        def open_dash():
            ACCENT_COLOR = pn.template.FastGridTemplate.accent_base_color
            XS = np.linspace(0, np.pi)

            def sine(freq, phase):
                return hv.Curve((XS, np.sin(XS * freq + phase))).opts(
                    responsive=True, min_height=400, title="Sine", color=ACCENT_COLOR
                ).opts(line_width=6)

            def cosine(freq, phase):
                return hv.Curve((XS, np.cos(XS * freq + phase))).opts(
                    responsive=True, min_height=400, title="Cosine", color=ACCENT_COLOR
                ).opts(line_width=6)

            freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
            phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)

            sine = pn.bind(sine, freq=freq, phase=phase)
            cosine = pn.bind(cosine, freq=freq, phase=phase)

            template = pn.template.FastGridTemplate(
                site="ThoroughZED Analytics", title="Relative Valuation Dashboard",
                header_color='red', header_background='black', theme='dark',
                main_layout='card',
                sidebar=[pn.pane.Markdown("## Settings"), freq, phase],
            )

            template.main[:3, :6] = pn.pane.HoloViews(hv.DynamicMap(sine), sizing_mode="stretch_both")
            template.main[:3, 6:] = pn.pane.HoloViews(hv.DynamicMap(cosine), sizing_mode="stretch_both")
            template.show()

        open_dash()



if __name__ == "__main__":
    while True:
        run_cli()
        run_again = input('> Enter another horse id? (y)es or (q) to quit ')
        if run_again.lower() == 'q':
            break
