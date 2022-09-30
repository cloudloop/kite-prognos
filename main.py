from ast import Continue
from genericpath import isfile
from textwrap import indent
from time import time
from pip._vendor import requests
import json
from pathlib import Path
import kitefuncs as k

#Point of interest: Enter location you want forcast for
lon = 63
lat = 22

#Creating a conditional function that checks if 1. There is a saved file available, and 2. if said file is the most current. If true on both, will make calculations based on saved file 
#instead of fetching new API data. 
if k.checkSaveRes(lon,lat):
    print("Save is available. Fetching...")
    data = k.getSavedLWF(lon,lat)
    k.findKitesurfDays(data)
else:
    k.makeAPIcall(lon,lat)
    
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
print(dt)