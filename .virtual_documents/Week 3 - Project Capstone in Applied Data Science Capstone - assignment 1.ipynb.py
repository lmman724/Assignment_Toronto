#import nescessary library
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

print('The library was import')


print("Hello Capstone Project Course")


url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

url = requests.get(url).text


data_canada_url = BeautifulSoup(url, 'html.parser')


df_canada_table_emply = []


data_canada_table_url = data_canada_url.find('table')


for row in data_canada_table_url.findAll('td'):
    cell = {}
    if row.span.text=='Not assigned':
        pass
    else:
        cell['PostalCode'] = row.p.text[:3]
        cell['Borough'] = (row.span.text).split('(')[0]
        cell['Neighborhood'] = (((((row.span.text).split('(')[1]).strip(')')).replace(' /',',')).replace(')',' ')).strip(' ')
        df_canada_table_emply.append(cell)


df_canada = pd.DataFrame(df_canada_table_emply)
df_canada.head()


# Export to csv and see all data incorrect on MS excel 
#df_canada.to_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/Canada_PostalCode.csv')


# Rename incorrect in Borough columns
df_canada['Borough']=df_canada['Borough'].replace({'Downtown TorontoStn A PO Boxes25 The Esplanade':'Downtown Toronto Stn A',
                                             'East TorontoBusiness reply mail Processing Centre969 Eastern':'East Toronto Business',
                                             'EtobicokeNorthwest':'Etobicoke Northwest','East YorkEast Toronto':'East York/East Toronto',
                                             'MississaugaCanada Post Gateway Processing Centre':'Mississauga'})


# see the shape of data
df_canada.shape



