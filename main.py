import kitefuncs as k
from datetime import datetime, date
import re
from geopy.geocoders import Nominatim
import os.path
from pathlib import Path
import controls  as controls

#Running controls scipt to ensure proper 
controls
#Adding ability to delete all directories created, thus remove alla saved data.
#controls.deleteAll()
"""
#Point of interest: Enter location you want forcast for
geolocator = Nominatim(user_agent="kite-prog")
location = geolocator.geocode("Schweizerbadet Dalarö")
lon = int(round(location.latitude,6))
lat = int(round(location.longitude,6))


#Creating a conditional function that checks if 1. There is a saved file available, and 2. if said file is the most current. If true on both, will make calculations based on saved file 
#instead of fetching new API data. 
if k.checkSaveRes(lon,lat):
    print("Save is available. Fetching...")
    data = k.getSavedLWF(lon,lat)
    k.findKitesurfDays(data)
else:
    k.makeAPIcall(lon,lat)

#[os.remove(file) for file in Path("responses/")]
#[os.remove(file) for file in Path("responses/")]


print(f"\nTime experiement starts here")
tt = "2022-09-28T21:00:00Z"
t = str(datetime.now())
print(t)
pattern = r"[-:.TZ ]"
t1 = re.split(pattern, t)
print(t1)
t1 = t1[:-1]
t2 = [int(t) for t in t1]
dt = date(t2[0],t2[1],t2[2])
tdy = date.today()
print(dt,tdy)

"""
