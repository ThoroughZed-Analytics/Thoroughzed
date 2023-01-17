import pandas as pd

sale_data = pd.read_csv("assets/example_data/sales_data.csv")
horse_db = pd.read_csv("assets/example_data/horse_db.csv")
#########################################################
trunc_horse_db = horse_db[['horse_id','genotype','bloodline','breed_type','color','birthday','super_coat','mother','father','horse_type']]
trunc_sale_data = sale_data[['currency','price','sold_at','token_id']]
trunc_sale_data = trunc_sale_data.rename(columns = {'token_id':'horse_id'})
merged = trunc_sale_data.copy()
merged = merged.merge(trunc_horse_db, on = "horse_id")
merged.to_csv('backup_meta_db.csv')