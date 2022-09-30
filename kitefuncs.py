
from time import time
from pip._vendor import requests
import json
from pathlib import Path

def apiCall(lon,lat):
    ###
    #Link to documentation https://opendata.smhi.se/apidocs/metfcst/get-forecast.html
    ###
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
    kitetimes = [time for time in weatherDict if weatherDict[time]["ws"] > 4 and weatherDict[time]["wd"] > 0 and weatherDict[time]["wd"] < 100]
    [print(f"Lets KIIIITESURF at:   {time} (ws={weatherDict[time]['ws']}, wd={weatherDict[time]['wd']})") for time in kitetimes]

def makeAPIcall(lon,lat):
    data = apiCall(lon,lat)
    saveData(lon,lat,data)
    wd = cherryPickData(data)
    saveCherryPick(lon,lat,wd)
    findKitesurfDays(wd)