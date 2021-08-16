import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import folium


# import data about assignment 2, we have 4 columns in dataframe after assignment 2 is PostalCode, Borough, Neighborhood, Latitude, Longtitude
df_canada = pd.read_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/data_canada_complete.csv')


df_canada.head()


address = 'Toronto, Canada'

geolocator = Nominatim(user_agent="Canada_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# create map of Manhattan using latitude and longitude values
map_canada = folium.Map(location=[latitude, longitude], zoom_start=11)
map_canada


# add markers to map
for lat, lng, label in zip(df_canada['Latitude'], df_canada['Longitude'], df_canada['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_canada)  
    
map_canada



