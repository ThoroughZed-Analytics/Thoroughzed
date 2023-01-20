import pandas as pd


meta_data_races = pd.read_csv("sales_and_stats_oliver.csv")
meta_data_attributes = pd.read_csv("data/master_data/backup_meta_db.csv")


print(f"columns of meta_data_races = \n {meta_data_races.columns}")
print(f"columns of meta_data_attributes = \n {meta_data_attributes.columns}")


merged = meta_data_attributes.copy()
merged = merged.merge(meta_data_races, on = "horse_id", how = "outer").fillna(0)

#merged.to_csv('sales_races_metadata.csv')

