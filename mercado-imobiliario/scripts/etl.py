
import pandas as pd
import numpy as np
import requests as r
from time import sleep
import functions
# Hiding Warnings Libs
import warnings
warnings.filterwarnings('ignore')


# Selecting cols
list_cols_details_data = ["ad_description","ad_id","house_rules","amenities","safety_features","number_of_bathrooms","number_of_bedrooms","number_of_beds","star_rating","number_of_guests","is_superhost","number_of_reviews","cleaning_fee","owner_id","response_rate_shown","guest_satisfaction_overall","picture_count"]
list_hosts_ids_itapema = ["host_id","host_rating","n_reviews","comments"]
list_mesh_ids_data_itapema = ["airbnb_listing_id","latitude","longitude"]
list_price_av_itapema = ["airbnb_listing_id","price","minimum_stay","mes"]



# details_data.to_parquet(f'datasets/parquet/Details_Data.parquet',index=False,compression="gzip")
# hosts_ids_itapema.to_parquet(f'datasets/parquet/Hosts_ids_Itapema.parquet',index=False,compression="gzip")
# mesh_ids_data_itapema.to_parquet(f'datasets/parquet/Mesh_Ids_Data_Itapema.parquet',index=False,compression="gzip")
try:
    details_data = pd.read_parquet(f'datasets/parquet/Details_Data.parquet')
    hosts_ids_itapema = pd.read_parquet(f'datasets/parquet/Hosts_ids_Itapema.parquet')
    mesh_ids_data_itapema = pd.read_parquet(f'datasets/parquet/Mesh_Ids_Data_Itapema.parquet')
except:
    details_data = pd.read_csv(f'datasets/Details_Data.csv', dtype=str, usecols=list_cols_details_data)
    details_data.drop_duplicates(subset='ad_id',keep='last',inplace=True)
    hosts_ids_itapema = pd.read_csv(f'datasets/Hosts_ids_Itapema.csv', dtype=str, usecols=list_hosts_ids_itapema)
    mesh_ids_data_itapema = pd.read_csv(f'datasets/Mesh_Ids_Data_Itapema.csv', dtype=str, usecols=list_mesh_ids_data_itapema)



# print(details_data.head())
# print(hosts_ids_itapema.head())
# print(mesh_ids_data_itapema.head())
# print(details_data.info())
# print(hosts_ids_itapema.info())
# print(mesh_ids_data_itapema.info())

# price_av_itapema = pd.read_csv(f'datasets/Price_AV_Itapema.csv',dtype=str,usecols=list_price_av_itapema)

# For optimize computer space
# price_av_itapema.to_parquet(f'datasets/parquet/Price_AV_Itapema.parquet',index=False,compression="gzip")

# Use if pyarrow and fastparquet are installed
try:
    price_av_itapema = pd.read_parquet(f'datasets/parquet/Price_AV_Itapema.parquet')
except:
    price_av_itapema = pd.read_csv(f'datasets/Price_AV_Itapema.csv',dtype=str,usecols=list_price_av_itapema)
    
print(price_av_itapema.head())
print()
print(price_av_itapema.shape)
print()
# print(price_av_itapema.info())

price_av_itapema2 = price_av_itapema.loc[price_av_itapema['mes'] == '12']
del(price_av_itapema)
price_av_itapema2.drop(columns='mes', inplace=True)




# deleting missing values because they represent less than 1% of dataset
price_av_itapema2 = price_av_itapema2.dropna()

print(price_av_itapema2.shape)
print()

price_av_itapema2['price'] = price_av_itapema2['price'].astype(np.float32)
price_av_itapema2['minimum_stay'] = price_av_itapema2['minimum_stay'].astype(np.int64)
df = pd.merge(details_data,hosts_ids_itapema,how='left',left_on='owner_id', right_on='host_id')



for index, row in enumerate(df['response_rate_shown']):
    if '%' not in str(row):
        if len(str(df.loc[index,'guest_satisfaction_overall'])) == 3 and str(df.loc[index,'guest_satisfaction_overall'])[0] == '1':
            df.loc[index,'response_rate_shown'] = df.loc[index,'guest_satisfaction_overall']+'%'       
        if len(str(df.loc[index,'guest_satisfaction_overall'])) < 3:
            df.loc[index,'response_rate_shown'] = df.loc[index,'guest_satisfaction_overall']+'%'
df.drop(columns='guest_satisfaction_overall', inplace=True)


df['safety_features'] = df['safety_features'].astype(str).apply(functions.cleaning)
df['house_rules'] = df['house_rules'].astype(str).apply(functions.cleaning)
df['comments'] = df['comments'].astype(str).apply(functions.cleaning)
df['ad_description'] = df['ad_description'].astype(str).apply(functions.cleaning)

df['n_safety_features'] = df['safety_features'].str.split(',').apply(len)
df['n_amenities'] = df['amenities'].str.split(',').apply(len)
df['n_house_rules'] = df['house_rules'].str.split(',').apply(len)
df['n_comments'] = df['comments'].str.split(',').apply(len)
df['n_ad_description'] = df['ad_description'].str.split(',').apply(len)


df.drop(['amenities','safety_features','house_rules','comments','ad_description'], axis=1, inplace=True)

df = pd.merge(df,mesh_ids_data_itapema,how='left',left_on='ad_id', right_on='airbnb_listing_id')
df.drop(columns=['owner_id', 'host_id','airbnb_listing_id'],inplace=True) 



sample = price_av_itapema2.sample(n=50000)
df = pd.merge(df, sample,how='left',left_on='ad_id', right_on='airbnb_listing_id')
df.drop(columns=['airbnb_listing_id'],inplace=True)


del(details_data)
del(hosts_ids_itapema)
del(mesh_ids_data_itapema)
del(price_av_itapema2)

print(df.shape)
print()
print(df.isnull().sum())
print()


# # removing columns that have many missing values and not relevant for this model
for col in df:
    if df[col].isnull().sum() > 30000:
        df = df.drop(col, axis=1)
print(df.isnull().sum())
print()
df.dropna(inplace=True)
print(df.shape)
print()
print(df.isnull().sum())
print()


df['number_of_bathrooms'] = df['number_of_bathrooms'].astype(np.float32, copy=False)
df['latitude'] = df['latitude'].astype(np.float32, copy=False)
df['longitude'] = df['longitude'].astype(np.float32, copy=False)
# df['number_of_bedrooms'] = df['number_of_bedrooms'].astype(np.float32, copy=False)
df['number_of_beds'] = df['number_of_beds'].astype(np.int64, copy=False)
df['number_of_guests'] = df['number_of_guests'].astype(np.int64, copy=False)
df['number_of_reviews'] = df['number_of_reviews'].astype(np.int64, copy=False)
df['cleaning_fee'] = df['cleaning_fee'].astype(np.float32, copy=False)
df['price'] = df['price'].astype(np.float32, copy=False)
df['minimum_stay'] = df['minimum_stay'].astype(np.int64, copy=False)

functions.box_diagram(df['price'])
functions.histogram(df['price'])

df, removed_rows = functions.del_outliers(df,'price')
print(f'{removed_rows} linhas removidas')
print()


functions.histogram(df['price'])
print(df.shape)
print()

df.to_csv(f'datasets/dataset_ML.csv',index=False)
print('Dataset saved!')