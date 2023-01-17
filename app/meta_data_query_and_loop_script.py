import pandas as pd
import time
import logging
import requests


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


#################################################################
sale_data = pd.read_csv("data/master_data/sales_data.csv")

# gets column from csv
sale_column = sale_data['token_id']

# removes duplicates
sale_column = set(sale_column)

# makes iterable
sale_column = list(sale_column)

# Get proper index
# sale_column = sale_column[0:17007] # harper

sale_column = sale_column[17007:34014] # oliver

# sale_column = sale_column[34014:] # jason
print(len(sale_column))

# initiates data frame with correct columns (schema)
# df = get_summary_horse_data(154936)

##################################################################

global df
df = pd.DataFrame()

def loop(counter=0):
    for x in sale_column[counter:len(sale_column)]:
        try:
            result = get_summary_horse_data(x)
            #print(result)
            print("ID, Counter: ", x, counter)
            global df
            df = pd.concat([df, result])
            counter += 1
            df.to_csv('all_horse_meta_oliver.csv')
            time.sleep(0.1)
        except:
            break
    if counter <= len(sale_column)-1:
        print("failed")
        time.sleep(30)
        loop(counter)



if __name__ == '__main__':
    print(f" press enter to start looping over {len(sale_column)} horse IDs")
    input('>')
    loop()
    df.to_csv('all_horse_meta_oliver.csv')
