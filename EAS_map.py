import pandas as pd 
import numpy as np
import json
from geopy.geocoders import Nominatim 
import requests 
import folium 
import streamlit as st 
from streamlit_folium import folium_static

data_all = pd.read_csv('Surabaya_Full_of_Data.csv')
data_geo = json.load(open('Kecamatan_Surabaya.geojson'))

#for changing to title only (first character is capital)
data_all['District'] = data_all['District'].str.title()
#for changing
data_all = data_all.replace({'District':'Pabean Cantikan'},'Pabean Cantian')
data_all = data_all.replace({'District':'Karangpilang'},'Karang Pilang')

def center():
   address = 'Surabaya, ID'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return latitude, longitude

#for changing type of the maps
add_select = st.sidebar.selectbox("What data do you want to see?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))
#for calling the function for getting center of maps
centers = center()
#showing the maps
map_sby = folium.Map(tiles=add_select, location=[runs[0], runs[1]], zoom_start=12)
#design for the app
st.title('Map of Surabaya')
folium_static(map_sby)

dicts = {"Total_Pop":'Total Population',
         "Male_Pop": 'Male Population',
         "Female_Pop": 'Female Population',
         "Area_Region": 'Areas Region(km squared)'}
select_data = st.sidebar.radio("What data do you want to see?"
("Total_Pop", "Area_Region","Male_Pop",'Female_Pop'))

def threshold(data):
   threshold_scale = np.linspace(data_all[dicts[data]].min(),
                              data_all[dicts[data]].max(),
                              10, dtype=float)
   # change the numpy array to a list
   threshold_scale = threshold_scale.tolist() 
   threshold_scale[-1] = threshold_scale[-1]
   return threshold_scale
def show_maps(data, threshold_scale):
   maps= folium.Choropleth(geo_data = data_geo,
                           data = data_all,
                           columns=['District',dicts[data]],
                           key_on='feature.properties.name',
                           threshold_scale=threshold_scale,
                           fill_color='YlOrRd',
                           fill_opacity=0.7,
                           line_opacity=0.2,
                           legend_name=dicts[data],
                           highlight=True,
                           reset=True).add_to(map_sby)
   folium_static(map_sby)
show_maps(select_data, threshold(select_data))

for idx in range(31):
    data_geo['features'][idx]['properties']['Total_Pop']= int(data_all['Total Population'][idx])
    data_geo['features'][idx]['properties']['Male_Pop'] = int(data_all['Male Population'][idx])
    data_geo['features'][idx]['properties']['Female_Pop'] = int(data_all['Female Population'][idx])
    data_geo['features'][idx]['properties']['Area_Region'] = float(data_all['Areas Region(km squared)'][idx])

def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        folium.LayerControl().add_to(map_sby)
        )
    maps.geojson.add_child(folium.features.GeoJsonTooltip
    (fields=['name',data],
    aliases=['District: ', 
    dicts[data]],
    labels=True))
    folium_static(map_sby)
show_maps(select_data, threshold(select_data))