import src.functions as func
import pandas as pd

url = 'https://es.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=mascarillas+ffp2&ltype=wholesale&SortType=total_tranpro_desc&groupsort=1&page='
page = 60

df = func.aliexpress_multiple_scraping (url, page)
df = df.replace('Not sales found', 0)
df['sales'] = df['sales'].astype(float)
df['price'] = [x.replace(',','.') for x in df.price]
df['price'] = df['price'].astype(float)
print(f'The number of total orders is {df.sales.sum()}')
print(f'The average price is {df.price.mean():.2f}')
print(df.shape)
df.to_csv(r'output/export_dataframe.csv', index=False)
