import pandas as pd


def clean_sales_data():
    df = pd.read_csv("assets/example_data/sales_data.csv")
    sales_df = df[['token_id', 'sold_at', 'price']]
    sales_df = sales_df.rename(columns={'token_id': 'horse_id', 'sold_at': 'time_sold'}).sort_values('horse_id')

    return sales_df


if __name__ == "__main__":
    print(clean_sales_data())
    