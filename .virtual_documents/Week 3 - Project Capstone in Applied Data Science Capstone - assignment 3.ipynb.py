import pandas as pd

import numpy as np

from geopy.geocoders import Nominatim

import folium

import requests

from sklearn.cluster import KMeans

import matplotlib.cm as cm
import matplotlib.colors as colors

import matplotlib.pyplot as plt

print("Libraries imported")


# import data about assignment 2, we have 4 columns in dataframe after assignment 2 is PostalCode, Borough, Neighborhood, Latitude, Longtitude
df_toronto = pd.read_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/data_canada_complete.csv')


df_toronto.head()


address = 'Toronto, Canada'

geolocator = Nominatim(user_agent="Canada_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# create map of Manhattan using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)
map_toronto


# add markers to map
for lat, lng, label in zip(df_toronto['Latitude'], df_toronto['Longitude'], df_toronto['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


df_toronto['Borough'].value_counts()


def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


CLIENT_ID = 'FSEB55GSJNOFADCDLXWPRQH4OJW2RWTBEGZF4INFJ4BNVYLH' # your Foursquare ID
CLIENT_SECRET = 'JOVA5LKXAFYOEYWCXEU1IX2QNT2IJIJX0IYNGZ1KF31GDO2G' # your Foursquare Secret
ACCESS_TOKEN = 'EWDRDJCFCIXM3X2RWXK0JF1HH3ETL4KDL5LQ5BPHTFINGRYP' # your FourSquare Access Token
VERSION = '20180604'
LIMIT = 30
code = 'BE5L1KYLVGNN1OJECTJGULAQSLY0RQA2A55O2WYUAEW5DRDM#_=_'
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)
print('Code:'+ code)
print('Access_token:'+ ACCESS_TOKEN)


# type your answer here
toronto_venues = getNearbyVenues(names=df_toronto['Neighborhood'],
                                   latitudes=df_toronto['Latitude'],
                                   longitudes=df_toronto['Longitude']
                                  )


print(toronto_venues.shape)
toronto_venues.head()


toronto_venues.groupby("Neighborhood").count().head()


print('There are {} uniques categories.'.format(len(toronto_venues['Venue Category'].unique())))


# one hot encoding
toronto_onehot = pd.get_dummies(toronto_venues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
toronto_onehot['Neighborhood'] = toronto_venues['Neighborhood'] 

# move neighborhood column to the first column
fixed_columns = [toronto_onehot.columns[-1]] + list(toronto_onehot.columns[:-1])
toronto_onehot = toronto_onehot[fixed_columns]

toronto_onehot.head()


toronto_grouped = toronto_onehot.groupby("Neighborhood").mean().reset_index()
toronto_grouped.head()


num_top_venues = 5

for hood in toronto_grouped['Neighborhood']:
    print("----"+str(hood)+"----")
    temp = toronto_grouped[toronto_grouped['Neighborhood'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted['Neighborhood'] = toronto_grouped['Neighborhood']

for ind in np.arange(toronto_grouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(toronto_grouped.iloc[ind, :], num_top_venues)

neighborhoods_venues_sorted.head()


# set number of clusters
kclusters = 5

toronto_grouped_clustering = toronto_grouped.drop('Neighborhood', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=None).fit(toronto_grouped_clustering)

# check cluster labels generated for each row in the dataframe

kmeans.labels_[0:10] 



neighborhoods_venues_sorted.info()


neighborhoods_venues_sorted.head()



#neighborhoods_venues_sorted.drop(['Cluster Labels'], axis=1, inplace=True)

# add clustering labels
neighborhoods_venues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

toronto_merged = df_toronto

neighborhoods_venues_sorted = neighborhoods_venues_sorted.astype(str)
# merge manhattan_grouped with manhattan_data to add latitude/longitude for each neighborhood
toronto_merged = toronto_merged.join(neighborhoods_venues_sorted.set_index('Neighborhood'), on='Neighborhood')


toronto_merged.head()


toronto_merged.shape


toronto_merged = toronto_merged.dropna()
toronto_merged['Cluster Labels'] = toronto_merged['Cluster Labels'].astype(int)


toronto_merged.shape


toronto_merged.to_csv('C:/Users/hp/Documents/Jupiter_Notebook/Applied Data Science Capstone/Assignment_Toronto_week 3/Assignment_Toronto/Ex3_final_toronto_neighborhood.csv')


# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(toronto_merged['Latitude'], toronto_merged['Longitude'], toronto_merged['Neighborhood'], toronto_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
         [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster - 1],
        fill=True,
        fill_color=rainbow[cluster - 1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters
