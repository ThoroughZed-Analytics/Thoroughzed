from app.get_intrinsic_value import get_intrinsic_value
from termcolor import colored
from assets.art import art
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from json import load



def run_cli():
    color_words = [colored('Horse/NFT ID', 'green', attrs=['bold']), colored("'q'", 'red', attrs=['bold']),
                   colored("> *** Not a valid ID! ***",'red', attrs=['blink']),
                   colored('(r)elative value', 'green'), colored('(i)ntrinsic value', 'green')]
    print(colored(art, 'green', attrs=['blink']))
    id = input(f"> Please enter the {color_words[0]} for the horse you'd like to evaluate or type {color_words[1]} to quit. ")
    if id.lower() == "q":
        exit()
    while not id.isdigit():
        print(f"{color_words[2]}")
        id = input(f"> Please enter the Horse/NFT ID for the horse you'd like to evaluate or type {color_words[1]} to quit. ")
        if id.lower() == "q":
            exit()
    choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit. ")
    if choice.lower() == "q":
        exit()
    while choice != "r" and choice != "i":
        print(f"{color_words[2]}")
        choice = input(f"> Would you like to find the {color_words[3]} or {color_words[4]}? Or type {color_words[1]} to quit. ")
        if id.lower() == "q":
            exit()
    if choice == "i":
        cost = input(f"> Enter the requested price of the horse in USD. Or type {color_words[1]} to quit. ")
        if cost.lower() == "q":
            exit()
        while not cost.isdigit():
            print("> *** Not a valid cost! ***")
            cost = input(f"> Enter the requested price of the horse in USD. Or type {color_words[1]} to quit. ")
            if cost.lower() == "q":
                exit()
        results = get_intrinsic_value(int(id), int(cost))
        print(colored('> Potential Net Earnings Per Race: ', 'green'), f'${results[0]}')
        print(colored('> Potential 3-Month Yield: ', 'green'), f"{results[1]}%")
        print(colored('> Races Needed to Cover Cost of Horse: ', 'green'), f"{results[2]}")
    if choice == "r":
        filename = 'app/dashboard_notebook.ipynb'
        with open(filename) as fp:
            nb = load(fp)

        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(line for line in cell['source'] if not line.startswith('%'))
                exec(source, globals(), locals())


if __name__ == "__main__":
    run_cli()
