import pandas as pd
import numpy as np
import functions
import requests as r
from time import sleep
import matplotlib.pyplot as plt



# viva_real_itapema.to_parquet(f'datasets/parquet/VivaReal_Itapema.parquet',index=False,compression="gzip")
try:
    viva_real_itapema = pd.read_parquet(f'datasets/parquet/VivaReal_Itapema.parquet')
    print(viva_real_itapema.head())
except:
    list_viva_real_itapema = ["listing_id","listing_desc","sale_price","amenities","total_area","bathrooms","bedrooms","suites","parking_spaces","address_zipcode","address_neighborhood","business_types","unit_type","usable_area"]
    viva_real_itapema = pd.read_csv(f'datasets/VivaReal_Itapema.csv',usecols=list_viva_real_itapema)
    viva_real_itapema.drop_duplicates(subset='listing_id',inplace=True)
    viva_real_itapema = viva_real_itapema.loc[viva_real_itapema['unit_type'] == 'APARTMENT']
    viva_real_itapema = viva_real_itapema.loc[viva_real_itapema['business_types'] != '["RENTAL"]']
    viva_real_itapema.drop(columns=['business_types','listing_id','unit_type'],inplace=True)



for index, i in enumerate(viva_real_itapema['total_area']):
    try:
        if 'nan' in str(i) and viva_real_itapema.loc[index,'usable_area'] == '0':
            pass
        else:
            viva_real_itapema.loc[index,'total_area'] = viva_real_itapema.loc[index,'usable_area']
    except:
        pass   

viva_real_itapema.drop(columns='usable_area',inplace=True)

viva_real_itapema['address_neighborhood'] = viva_real_itapema['address_neighborhood'].astype(str).apply(functions.cleaning)
viva_real_itapema['n_amenities'] = viva_real_itapema['amenities'].str.split(',').apply(len)

print(viva_real_itapema.shape)
print()
print(viva_real_itapema.isnull().sum())
print()

viva_real_itapema, linhas_removidas = functions.del_outliers(viva_real_itapema,'sale_price')
print(f'{linhas_removidas} linhas removidas')
print()


viva_real_itapema['m²'] = viva_real_itapema['sale_price'] / viva_real_itapema['total_area']
# print(viva_real_itapema.describe())


viva_real_itapema['m²'] = viva_real_itapema['m²'].fillna(viva_real_itapema['m²'].mean())
list_unique_cep = []
for index, i in enumerate(viva_real_itapema['address_neighborhood']):
    try:
        if 'Nan' in str(i):
            if viva_real_itapema.loc[index,'address_zipcode'] not in list_unique_cep:
                list_unique_cep.append(int(viva_real_itapema.loc[index,'address_zipcode']))
    except:
        pass

list_location = []
list_consult = []
list_cep = []

for i in list_unique_cep:
    res = r.get(f'https://viacep.com.br/ws/{i}/json/')
    list_consult.append(res.json())
    sleep(30)

for i in list_consult:
    list_cep.append(i['cep'])
    if i['bairro'] != '':
        list_location.append(i['bairro'])
    else:
        list_location.append(i['localidade'])

df_location = pd.DataFrame({'zip_code':list_cep, 'location':list_location})
df_location['zip_code'] = df_location['zip_code'].astype(str).apply(functions.cleaning)
df_location['zip_code'] = df_location['zip_code'].astype(np.float32)
    

viva_real_itapema2 = pd.merge(viva_real_itapema, df_location, how='left', left_on='address_zipcode', right_on='zip_code')

for index, i in enumerate(viva_real_itapema2['address_neighborhood']):
    if 'Nan' in str(i):
        viva_real_itapema2.loc[index,'address_neighborhood'] = viva_real_itapema2.loc[index,'location']
        
viva_real_itapema2.drop(columns=['address_zipcode','zip_code','location'],inplace=True)

viva_real_itapema2[['address_neighborhood','sale_price']].groupby('address_neighborhood').median().sort_values(by='sale_price', ascending=False)


# grouped_address = viva_real_itapema2.groupby('address_neighborhood')
# plt.figure(1)
# grouped_address['sale_price'].median().sort_values(ascending=False).plot.bar(figsize = (18,8),
#                                                                       color = ['#836FFF'],
#                                                                       title = 'Price in Millions (Median)')


# plt.figure(1)
# grouped_address['sale_price'].sum().sort_values(ascending=False).plot.bar(figsize = (18,8),
#                                                                       color = ['#836FFF'],
#                                                                       title = 'Price in Millions (SUM)')
print('Result of graphs in the report.')