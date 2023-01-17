import requests
import pandas as pd
import logging
import time

logging.basicConfig(filename='error.log', level=logging.ERROR)

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
    print(response)

    # Transform data into json format
    summary_horse_data = response.json()
    
    # flattens json
    summary_horse_data = pd.json_normalize(summary_horse_data)
    print(f'running for {horse_id}')
    return summary_horse_data


if __name__ == '__main__':
    # horse_id = input('> enter horse id: ')
    horse_id = 8919
    meta_data = get_summary_horse_data(int(horse_id))


    meta_data.to_csv('assets/example_data/horse_meta_data.csv')
