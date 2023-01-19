from app.get_intrinsic_value import get_intrinsic_value
from termcolor import colored
from assets.art import art
from app.get_relative_value import get_relative_value
from app.model_predict import predict_horse_price
from app.meta_data_query_and_loop_script import get_summary_horse_data
import numpy as np
import panel as pn
import holoviews as hv
pn.extension('tabulator')


color_words = [colored('Horse/NFT ID', 'green', attrs=['bold']),
               colored("'q'", 'red', attrs=['bold']),
               colored("> *** Not a valid input! ***", 'red', attrs=['blink']),
               colored('(r)elative value', 'green'), colored('(i)ntrinsic value', 'green'),
               colored("'h'", 'red', attrs=['bold']),
               colored("> *** This horse has not been raced and cannot have a valuation run on its performance ***", 'red', attrs=['bold']),
               colored("> *** Not a valid Horse/NFT ID in ZED Run ***", 'red', attrs=['bold']),
               colored("'y'", 'green', attrs=['bold']),
               colored("'n'", 'red', attrs=['bold']),
               colored("> *** Type 'CTRL + C' to exit the online dashboard. ***", 'red', attrs=['blink'])]
valid = True


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


def check_id(id):
    if id.lower() == "q":
        print("> Thanks for using ThoroughZED!")
        return "exit"
    while not id.isdigit():
        if id.lower() == "q":
            print("> Thanks for using ThoroughZED!")
            return "exit"
        if id.lower() == "h":
            help()
        else:
            print(f"\n{color_words[2]}\n")
        id = input(f"> Please enter the Horse/NFT ID for the horse you'd like to evaluate. Or type {color_words[1]} to quit or {color_words[5]} for help. ")
    return id


def check_valid_horse(id):
    global valid
    try:
        horse_object = get_summary_horse_data(int(id))
        if horse_object['data.horse.race_statistic.number_of_races'][0] == 0:
            print(f"\n{color_words[6]}\n")
            answer = input(f"> Would you like to run a relative valuation on this horse? Type {color_words[8]} for yes or {color_words[9]} for no. ")
            while answer.lower() != "y" and answer.lower() != "n":
                print(f"\n{color_words[2]}\n")
                answer = input(f"> Would you like to run a relative valuation on this horse? Type {color_words[8]} for yes or {color_words[9]} for no. ")
            if answer.lower() == "n":
                return "start-over"
            if answer.lower() == "y":
                valid = False
                return id
        valid = True
        return id
    except:
        print(f"\n{color_words[7]}\n")
        return "start-over"


def check_choice(choice):
    if choice.lower() == "q":
        print("> Thanks for using ThoroughZED!")
        return "exit"
    while choice.lower() != "r" and choice.lower() != "i":
        if choice.lower() == "q":
            print("> Thanks for using ThoroughZED!")
            return "exit"
        if choice.lower() == "h":
            help()
        else:
            print(f"\n{color_words[2]}\n")
        choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit or {color_words[5]} for help. ")
    return choice


def check_price(cost):
    if cost.lower() == "q":
        print("> Thanks for using ThoroughZED!")
        return "exit"
    while not cost.isdigit():
        if cost.lower() == "q":
            print("> Thanks for using ThoroughZED!")
            return "exit"
        else:
            print(f"\n{color_words[2]}\n")
        cost = input(f"> Enter the listing price of the horse in USD. Or type {color_words[1]} to quit. ")
    return cost


def relative(id):
    result = predict_horse_price(int(id))
    print(f"\n> Result: {result}\n")
    answer = input(f"> Would you like to display the dashboard? Type {color_words[8]} for yes or {color_words[9]} for no. ")
    while answer.lower() != 'y' and answer.lower() != 'n':
        print(f"\n{color_words[2]}\n")
        answer = input(f"> Would you like to display the dashboard? Type {color_words[8]} for yes or {color_words[9]} for no. ")
    if answer.lower() == 'y':
        print(f"\n{color_words[10]}\n")

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


def intrinsic(id, cost):
    results = get_intrinsic_value(int(id), int(cost))
    if float(results[0]) >= 0:
        print('\n> Potential Net Earnings Per Race: ', colored(f'${results[0]}', 'green'))
    else:
        print('\n> Potential Net Earnings Per Race: ', colored(f'${results[0]}', 'red'))
    if float(results[1]) >= 0:
        print('> Potential 3-Month Yield: ', colored(f'{results[1]}%', 'green'))
    else:
        print('> Potential 3-Month Yield: ', colored(f'{results[1]}%', 'red'))
    if float(results[2]) >= 0:
        print('> Races Needed to Cover Cost of Horse: ', colored(f'{"{0:,}".format(results[2])}', 'green'), '\n')
    else:
        print('> Races Needed to Cover Cost of Horse: ', colored(f'{"{0:,}".format(results[2])}', 'red'), '\n')


def run_cli():
    print(colored(art, 'green', attrs=['blink']))
    id = input(f"> Please enter the {color_words[0]} for the horse you'd like to evaluate. Or type {color_words[1]} to quit or {color_words[5]} for help. ")
    id = check_id(id)
    if id == "exit":
        exit()
    id = check_valid_horse(id)
    if id == "exit":
        exit()
    if id != "start-over":
        if not valid:
            relative(id)
        else:
            choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit or {color_words[5]} for help. ")
            choice = check_choice(choice)
            if check_choice(choice) == "exit":
                exit()
            if choice == "r":
                relative(id)
            if choice == "i":
                cost = input(f"> Enter the listing price of the horse in USD. Or type {color_words[1]} to quit. ")
                cost = check_price(cost)
                if cost == "exit":
                    exit()
                intrinsic(id, cost)


if __name__ == "__main__":
    while True:
        run_cli()
        run_again = input(f'> Enter another horse id? Type {color_words[8]} for yes or {color_words[9]} for no. ')
        if run_again.lower() == 'n':
            print("> Thanks for using ThoroughZED!")
            break
