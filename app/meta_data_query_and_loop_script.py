import sys
import requests
import logging
import backoff
import pandas as pd
import json
from pandas import json_normalize
import time


logging.basicConfig(filename='error.log', level=logging.ERROR)


############################################

def get_summary_horse_data(horse_id):
    
    base_url = "https://zed-ql.zed.run/graphql"

    query = """
    query($input: HorseInput) {
        horse(input: $input) {
            name
            nft_id
            img_url
            gen
            bloodline
            breed_type
            color
            inserted_at
            super_coat
            horse_type
            race_statistic {
                first_place_finishes
                second_place_finishes
                third_place_finishes
                number_of_races
                win_rate
                number_of_free_races
                number_of_paid_races
                free_win_rate
                paid_win_rate
            }
            parents{
                name
                nft_id
            }
        }
    }
    """

    variables = {
        "input": {
            "horse_id": horse_id
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "variables": variables
    }

    # Execute the POST query to GraphQL endpoint
    response = requests.post(base_url, json=payload, headers=headers)
    # print(response.status_code)

    # Transform data into json format
    summary_horse_data = response.json()
    
    # flattens json
    summary_horse_data = pd.json_normalize(summary_horse_data)

    # print(f'running for {horse_id}')

    return summary_horse_data

@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def get_horse_data(horse_id):
    base_url = 'https://api.zed.run/api/v1/races/horse_stats'

    payload = {
        "content-type": "application/json"
    }

    variables = {
        "horse_id": horse_id
    }

    response = requests.get(base_url, json=payload, params=variables)

    response_json = response.json()

    flat_response = json_normalize(response_json)
    return flat_response
##################################################################

# global df
# df = pd.DataFrame()

# def loop(counter=0):
#     for x in sale_column[counter:len(sale_column)]:
#         try:
#             result = get_summary_horse_data(x)
#             #print(result)
#             print("ID, Counter: ", x, counter)
#             global df
#             df = pd.concat([df, result])
#             counter += 1
#             df.to_csv('all_horse_meta_oliver.csv')
#             time.sleep(0.1)
#         except:
#             break
#     if counter <= len(sale_column)-1:
#         print("failed")
#         time.sleep(30)
#         loop(counter)



if __name__ == '__main__': 
    
    sale_data = pd.read_csv("data/master_data/sales_data.csv")

    # gets column from csv
    sale_column = sale_data['token_id']

    # removes duplicates
    sale_column = set(sale_column)

    # makes iterable
    horses = list(sale_column) # len(horses) = 51021
    
    # Get proper index
    # horses = horses[0:12756] # harper
    # horses = horses[12756:25511] # oliver
    horses = horses[25511:38266] # jason
    # horses = horses[38266:] # dennis

    query_df = pd.DataFrame()
    
    i = 0

    while i < len(horses):
        id = horses[i]
        try:
            horse_query_result = get_horse_data(id)
            horse_query_result = horse_query_result.assign(horse_id=id)
            query_df = pd.concat([query_df, horse_query_result])
            query_df = query_df.drop((['win_place.place', 'win_place.races', 'win_place.wins', 'last_five']), axis=1)
            
            print(query_df.tail(1), f"count: {i}")
            
            query_df.to_csv('sales_and_stats_jason.csv')
            
            time.sleep(0.1)
            i += 1
       
        except KeyboardInterrupt:
            print("\nScript interrupted by user. Exiting...")
            sys.exit()
       
        except:
            time.sleep(15)
            continue
