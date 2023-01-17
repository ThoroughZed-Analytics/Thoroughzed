from get_horse_meta_create_csv import get_summary_horse_data
import pandas as pd
import time
import logging


logging.basicConfig(filename='error.log', level=logging.ERROR)

sale_data = pd.read_csv("example_data/sales_data.csv")

# gets column from csv
sale_column = sale_data['token_id']

# removes duplicates
sale_column = set(sale_column)

# makes iterable
sale_column = list(sale_column)

# initiates data frame with correct columns (schema)
# df = get_summary_horse_data(154936)

global df
df = get_summary_horse_data(154936)

def loop(counter=0):
    for x in sale_column[counter:len(sale_column)]:
        try:
            result = get_summary_horse_data(x)
            print("ID, Counter: ", x, counter)
            global df
            df = pd.concat([df, result])
            counter += 1
            time.sleep(0.1)
        except:
            break
    if counter <= len(sale_column):
        print("restarting")
        time.sleep(10)
        loop(counter)


loop()

df.to_csv('all_horse_meta.csv')
