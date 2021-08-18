import pandas as pd
import numpy as np



# read csv canada file consist of three columns: PostalCode, Borough, and Neighborhood (file complete cleaning on assignment 1)
df_canada = pd.read_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/Canada_PostalCode.csv')


df_canada.head()


postal_code = df_canada["PostalCode"]


# read csv canada file consist of three columns: PostalCode, Latitude and Longtitude (file provice by intructor assignment)
# I have try using geospatial code but the code run a lot of time so I using dataset on assignment
df_canada_geospatial = pd.read_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/Geospatial_Coordinates.csv')


df_canada_geospatial.head()


df_canada.columns


df_canada_geospatial.columns


#Using merged function in connect two dataframe have key_id is postal_code 
merged_df_data_canada = pd.merge(left= df_canada, right= df_canada_geospatial, left_on= 'PostalCode', right_on= "Postal Code")


merged_df_data_canada =merged_df_data_canada.drop(['Postal Code'], axis= 1)


merged_df_data_canada.head()


merged_df_data_canada.to_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/data_canada_complete.csv')
