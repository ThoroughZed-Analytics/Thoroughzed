import requests
import pandas as pd
import time



start_count = 0

def get_summary_horse_data(horse_id, proxy, global_counter):
    
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
    counter = global_counter
    status_code = 0
    while status_code != 200 and counter < len(proxies):
        try:
            print(f'trying: {proxies[counter]}')
            response = requests.post(base_url, json=payload, headers=headers,
                                     proxies={'http': proxies[counter], 'https': proxies[counter]})
            status_code = response.status_code
            time.sleep(0.1)
            if response.status_code == 200:
                print(f'Successful proxy: {proxies[counter]}')
                global start_count
                start_count += 1
                start_count = start_count % 7
        except Exception as e:
            print(e, horse_id)
            counter += 1
            pass

    # Transform data into json format
    summary_horse_data = response.json()
    
    # flattens json
    summary_horse_data = pd.json_normalize(summary_horse_data)
    print(f'running for {horse_id}')
    return summary_horse_data


sale_data = pd.read_csv("example_data/sales_data.csv")

# gets column from csv
sale_column = sale_data['token_id']

# removes duplicates
sale_column = set(sale_column)

# makes iterable
sale_column = list(sale_column)

with open('good_proxies.txt', 'r') as f:
    proxies = f.read().split('\n')

df = pd.DataFrame()


for x in sale_column:
    try:
        # global start_count
        result = get_summary_horse_data(x, proxies, start_count)
        print(result)
        print("ID: ", x)
        df = pd.concat([df, result])
        df.to_csv('all_horse_meta_small_sample.csv')
        # time.sleep(0.1)
    except Exception as e:
        print(e)
        continue
