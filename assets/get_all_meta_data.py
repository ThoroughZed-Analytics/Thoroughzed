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
df = get_summary_horse_data(154936)

sale_column_sub = sale_column[1:201]

# loops

# chunk_size = 30
# delay = 0.1
# chunk_wait = 15
#
# for i in range(0, len(sale_column_sub), chunk_size):
#     chunk = sale_column_sub[i:i+chunk_size]
#     for id_var in chunk:
#         try:
#             result = get_summary_horse_data(id_var)
#             time.sleep(delay)
#         except Exception as e:
#             print(e)
#             logging.exception("An error occured")
#         else:
#             df = pd.concat([df, result])
#         finally:
#             print('moving to next horse')
#     time.sleep(chunk_wait)

# for x in sale_column[1:200]:
#     try:
#         result = get_summary_horse_data(x)
#         time.sleep(.1)
#     except Exception as e:
#         print(e)
#         logging.exception("An error occured")
#     else:
#         df = pd.concat([df, result])
#     finally:
#         print('moving to next horse')

df.to_csv('all_horse_meta.csv')
