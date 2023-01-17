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
		last_breeding_reset
		breeding_counter
		horse_type
		race_statistic {
			first_place_finishes
			second_place_finishes
			third_place_finishes
			number_of_races
			win_rate
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
    
    # Transform data into json format
    summary_horse_data = response.json()
    
    # flattens json
    summary_horse_data = pd.json_normalize(summary_horse_data)
    print(f'running for {horse_id}')
    return summary_horse_data


if __name__ == '__main__':
    # horse_id = input('> enter horse id: ')
    horse_id = 393554
    meta_data = get_summary_horse_data(int(horse_id))


    meta_data.to_csv('example_data/horse_meta_data.csv')