from ast import Continue
from genericpath import isfile
from textwrap import indent
from time import time
from pip._vendor import requests
import json
from pathlib import Path
from datetime import datetime

###
#Link to documentation https://opendata.smhi.se/apidocs/metfcst/get-forecast.html
###

#Point of interest: Enter location you want forcast for
lon = 59
lat = 18

def apiCall(lon,lat):
    #Setting up API call function for SMHI forcast on location
    #See https://opendata.smhi.se/apidocs/metfcst/parameters.html
    smhi_url = "https://opendata-download-metfcst.smhi.se"
    Sthlm_Lat = str(lon)
    Sthlm_Lon = str(lat)
    full_url = smhi_url+f"/api/category/pmp3g/version/2/geotype/point/lon/{Sthlm_Lon}/lat/{Sthlm_Lat}/data.json"
    response = requests.get(full_url, verify=False)
    status = response.raise_for_status()
    data = response.json()
    return data

def saveData(lon,lat,data):
    #Saving local file with indent to better analys json response.
    with open(f"responses/responseLon{lon}Lat{lat}.json","w") as f:
        f.write(json.dumps(data,indent=4))

def cherryPickData(data):
    #Finding position of values of interest: 
    #Fetching data for variable positions of wd, ws, gust, wsymb2 in fetched json
    weatherDict={}
    for j in range(len(data["timeSeries"])):
        time = data["timeSeries"][j]["validTime"]
        wd = [data["timeSeries"][j]["parameters"][i]["values"][0] for i in range(len(data["timeSeries"][j]["parameters"])) if data["timeSeries"][j]["parameters"][i]["name"] == "wd"][0]
        ws = [data["timeSeries"][j]["parameters"][i]["values"][0] for i in range(len(data["timeSeries"][j]["parameters"])) if data["timeSeries"][j]["parameters"][i]["name"] == "ws"][0]
        gust = [data["timeSeries"][j]["parameters"][i]["values"][0] for i in range(len(data["timeSeries"][j]["parameters"])) if data["timeSeries"][j]["parameters"][i]["name"] == "gust"][0]
        wsymb2 = [data["timeSeries"][j]["parameters"][i]["values"][0] for i in range(len(data["timeSeries"][j]["parameters"])) if data["timeSeries"][j]["parameters"][i]["name"] == "Wsymb2"][0]
        weatherDict[time] = {"wd": wd, "ws": ws, "gust": gust, "wsymb2": wsymb2}
        #print(f"{time}: {weatherDict[time]}\n")
    return weatherDict

def saveCherryPick(lon,lat,weatherD):
    with open(f"localWindForcast/lwf-Lon{lon}Lat{lat}.json","w") as f:
        f.write(json.dumps(weatherD,indent=4))

def checkSaveRes(lon,lat):
    print("Checking saves...")
    file = Path(f"responses/responseLon{lon}Lat{lat}.json")
    if file.exists():
        print("A json file exists!!")
        return True

def getSavedLWF(lon,lat):
    with open(f"localWindForcast/lwf-Lon{lon}Lat{lat}.json","r") as f:
        data = json.loads(f.read())
        return data

def findKitesurfDays(weatherDict):
    #Conditional review of weatherdict to identify potential kitesurf dates
    kitetimes = [time for time in weatherDict if weatherDict[time]["ws"] > 6 and weatherDict[time]["wd"] > 0 and weatherDict[time]["wd"] < 100]
    [print(f"Lets KIIIITESURF at:   {time} (ws={weatherDict[time]['ws']}, wd={weatherDict[time]['wd']})") for time in kitetimes]

def makeAPIcall(lon,lat):
    data = apiCall(lon,lat)
    wd = cherryPickData(data)
    saveData(lon,lat,data)
    saveCherryPick(lon,lat,wd)
    findKitesurfDays(wd)

#Creating a conditional function that checks if 1. There is a saved file available, and 2. if said file is the most current. If true on both, will make calculations based on saved file 
#instead of fetching new API data. 
if checkSaveRes(lon,lat):
    print("Save is available. Fetching...")
    data = getSavedLWF(lon,lat)
    findKitesurfDays(data)
else:
    makeAPIcall(lon,lat)

t = '2022-09-28T20:00:00Z'
dt_obj = datetime.fromisoformat('2020-01-06T00:00:00.000Z'[:-1] + '+00:00')
dt2 = datetime.datetime(2020, 1, 6, 0, 0, tzinfo=datetime.timezone.utc)
print([dt_obj, type(dt_obj)])
print([dt2, type(dt2)])