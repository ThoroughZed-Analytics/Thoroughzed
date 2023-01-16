from get_horse_meta_create_csv import get_summary_horse_data
import pandas as pd
import time


sale_data = pd.read_csv("assets/example_data/sales_data.csv")

# gets column from csv
sale_column = sale_data['token_id']

# removes duplicates
sale_column = set(sale_column)

# makes iterable
sale_column = list(sale_column)

# initiates data frame with correct columns (schema)
df = get_summary_horse_data(154936)

# loops
for x in sale_column[1:10]:
    result = get_summary_horse_data(x)
    df = pd.concat([df, result])
    time.sleep(.1)


df.to_csv('all_horse_meta.csv')
