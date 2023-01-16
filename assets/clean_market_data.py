import pandas as pd
from datetime import datetime


def to_hours(time):
    return (time // 3600) + 6


def clean_sales_data():
    df = pd.read_csv("example_data/sales_data.csv")
    sales_df = df[['token_id', 'sold_at', 'price']]
    sales_df = sales_df.rename(columns={'token_id': 'horse_id', 'sold_at': 'time_sold'}).sort_values('horse_id').reset_index()
    sales_df['time_sold'] = sales_df['time_sold'].apply(to_hours)

    return sales_df


if __name__ == "__main__":
    print(clean_sales_data())
