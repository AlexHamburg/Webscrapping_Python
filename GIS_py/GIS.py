import folium
import pandas as pd
import json

# Create map with light background
map = folium.Map(location=[53.551086, 9.993682], zoom_start=11, tiles="Mapbox Bright")

# Get a csv with prices
prices = pd.read_csv("Hamburg_prices.csv", encoding="latin1")

# Max price in the city - as param for color
max_price_hamburg = prices["Average_Price"].max()

# convert all into lists
districts = list(prices["District"])
prices_list = list(prices["Average_Price"])
name_districts_from_json = []
coord_from_json = []
del prices

# convert a 2D array into 1D array for folium.Marker
def get_coord(x):
    lon = []
    lat = []
    for i in x:
        lon.append(i[0])
        lat.append(i[1])
    result=[]
    result.append(sum(lat)/len(lat))
    result.append(sum(lon)/len(lon))
    return result

# get a name of districts and coordinates from json
with open('Hamburg.json') as f:
    data = json.load(f)
for x in data["features"]:
    name_districts_from_json.append(x["properties"]["name"])
    coord_from_json.append(get_coord(x["geometry"]["coordinates"][0][0]))

# convert info into string for popup of markers
def get_popup(x):
    if (x in districts):
        result = x + ": " + str(float("{0:.2f}".format(prices_list[districts.index(x)]))) + " EUR pro m2"
    else:
        result = x
    return result

feature_group = folium.FeatureGroup(name="Prices")

# add districts as polygons
feature_group.add_child(folium.GeoJson(data=open("Hamburg.json", "r", encoding="utf-8-sig").read(), name="Hamburg real estate",
                                       style_function=lambda x: {
                                           "fillOpacity": prices_list[districts.index(x["properties"]["name"])] / max_price_hamburg if x["properties"]["name"] in districts else 0,
                                            "fillColor":"#00ff00",
                                            "weight": 0.5}))
# add Markers with popups (info: name of district and price)
for x, y in zip(coord_from_json, name_districts_from_json):
    feature_group.add_child(folium.Marker(location=x, popup=get_popup(y), icon=folium.Icon(color="green")))

map.add_child(feature_group)

map.save("Map_test.html")
