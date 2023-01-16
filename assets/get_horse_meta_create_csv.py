import requests
import pandas as pd
import json

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
		offsprings {
			bloodline
			breed_type
			color
			gen
			horse_type
			nft_id
			race_statistic {
				first_place_finishes
				second_place_finishes
				third_place_finishes
				number_of_races
				win_rate
				positions_per_distance{
					distance
					positions{
						frequency
						position
					}
				}
			}
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
    # Transform data into string that can be read by pandas


    #summary_horse_data = json.dumps(summary_horse_data)


    return pd.json_normalize(summary_horse_data, sep='_')


if __name__ == '__main__':
    # horse_id = input('> enter horse id: ')
    horse_id = 154936
    meta_data = get_summary_horse_data(int(horse_id))
    #df = pd.read_json(meta_data)
    df = pd.json_normalize(meta_data, sep='_')

    print(df)
    #print(meta_data.items())
    df.to_csv('assets/example_data/horse_meta_data.csv')