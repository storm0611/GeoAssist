"""


         Version to show (demo).



Created on Sun Mar 27 15:00:00 2022
@author: Michele Martignago - martignagomichele@gmail.com

"""

import openrouteservice
from openrouteservice import convert
import folium
#import json
import pandas as pd
import numpy as np
#import datetime
from datetime import date
import xlrd
  


client = openrouteservice.Client(key='5b3ce3597851110001cf6248f0060529d8d9431b9337cd87a67af098')

n_next = 50

data = pd.read_excel (r'dati.xltx', sheet_name = 'Rubr', nrows=n_next+1)
#address_via = pd.DataFrame(data, columns= ['Via'])
#address_city = pd.DataFrame(data, columns= ['Loc'])

#coords = data['coord'].tolist()

lat = data['lat']
long = data['long']
next_deadline = data['next_deadline']



lat = list(np.float_(lat))
long = list(np.float_(long))
#next_deadline = list(np.float_(next_deadline))

#coords = [(long_, lat_) for lat_ in lat for long_ in long] 
lat= lat[0:n_next]
long= long[0:n_next]
next_deadline = next_deadline[0:n_next]
#coords = coord[0:25]
#print(coords)

#initialize new variable that will have date in DD/MM/YYYY
next_deadline_DD = next_deadline

for i in range(n_next):
    xl_date = next_deadline[i]
    datetime_date = xlrd.xldate_as_datetime(xl_date, 0)
    date_object = datetime_date.date()
    string_date = date_object.isoformat()
    next_deadline_DD[i] = date_object

coords = [(p1, p2) for idx1, p1 in enumerate(long) for idx2, p2 in enumerate(lat) if idx1==idx2]
#set location coordinates in longitude,latitude order
# be aware that google maps usually gives you lat, long, so we enter like that and then swap x y
#coords = ((45.73600000000000,12.43487500000000),(45.87493900000000,11.94283900000000),(45.8582068,11.8771237))
#coords = ((coords_1[2]), (coords[1]))
#coords = [(y, x) for x, y in coords]

print(coords)

urgency = [None]*len(next_deadline_DD)
oggi = date.today()
print(oggi)
for i in range(len(next_deadline_DD)):
    urgency[i] = next_deadline_DD[i] - oggi #(hours=-8)
    #urgency[i] = urgency[i].isoformat()
    print(urgency[i].days)

#coords = ((80.21787585263182,6.025423265401452),(80.23990263756545,6.018498276842677))

######################
##### Risolve problema di Routing
######################
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

print(distance_txt)

##### Plot con risoluzione
m2 = folium.Map(location=[45.736000000000,12.434875000000],zoom_start=9, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=400)).add_to(m2)
'''

##### Plot senza risoluzione
m2 = folium.Map(location=[45.736000000000,12.434875000000],zoom_start=9, control_scale=True,tiles="cartodbpositron")
#folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m2)


''' 


###########
# Markers non iterati ma dichiarati singolarmente
###########
'''
folium.Marker(
    location=list(coords[0][::-1]),
    popup="Power On",
    icon=folium.Icon(color="orange"),
).add_to(m2)

folium.Marker(
    location=list(coords[1][::-1]),
    popup= f"Num_GE \n Cliente_1 \n Entro gg/mm/aa \n via indirizzo numero Paese PROV \n 337 52xx529 \n {coords[1][::-1]} ok ",
    icon=folium.Icon(color="red"),
).add_to(m2)

folium.Marker(
    location=list(coords[2][::-1]),
    popup= f"Num_GE \n Cliente_2 \n Entro gg/mm/aa \n via indirizzo numero Paese PROV \n 337 52xx529 \n {coords[2][::-1]} ok ",
    icon=folium.Icon(color="purple"),
).add_to(m2)
'''




####################
# Iterated Markers
####################
'''
for i in range(len(coords)):
    
    folium.Marker(
        #text = f"Num_GE \n Cliente_ \n Entro {urgency[i].days} gg i.e.: {next_deadline[i]} \n via indirizzo numero Paese PROV \n  337 52xx529 \n  {coords[i][::-1]} ok",
        location=list(coords[i][::-1]),
        #iframe = folium.IFrame(text),
        popup = folium.Popup(min_width=500, max_width=800),
        icon=folium.Icon(color="purple"),
        ).add_to(m2)
'''
"""
text = urgency
for i in range(n_next):
    text[i]= f"Num_GE \n Cliente_2 \n Entro {urgency[i].days} giorni \n ovvero {next_deadline_DD[i]} \n via indirizzo numero Paese PROV \n 337 52xx529 \n {coords[i][::-1]} ok ",


for lt, ln, name in zip(lat, long, text):
    m2.add_child(folium.Marker(location=[lt, ln], popup=str(name), icon=folium.Icon(color='green', max_width=100, min_width=100)))
"""


marker_colors = [None]*len(urgency)


for i in range(len(urgency)):
    if urgency[i].days < 0:
        marker_colors[i] = 'red'
    elif urgency[i].days  < 25:
        marker_colors[i] = 'orange'
    elif urgency[i].days  <90:
        marker_colors[i] = 'green'
    else:
        marker_colors[i] = 'blue'   


for i in range(n_next):
    iframe = folium.IFrame('GE numero:' + '<br>' + 'Cliente:  ' + '<br>' + 'Entro:  ' + str(urgency[i].days) + ' gg' + '<br>' + 'Entro:  ' + str(next_deadline_DD[i]) + '<br>'  + 'Lat:  ' + str(lat[i]) + '<br>' + 'Lon:  ' + str(long[i]) +  '<br>' + 'Telefono:')
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    #folium.Marker(location=[lat[i], long[i]], icon=folium.Icon(color='blue', icon='map-marker', prefix='fa'), popup=popup).add_to(m2)
    folium.Marker(location=[lat[i], long[i]], icon=folium.Icon(color=marker_colors[i], icon='map-marker', prefix='fa'), popup=popup).add_to(m2)



m2.save('map2.html')