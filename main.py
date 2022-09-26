from ast import Continue
from textwrap import indent
from pip._vendor import requests
import json
#from requests import requests

###
#Link to documentation https://opendata.smhi.se/apidocs/metfcst/get-forecast.html


#Point of interest: Enter location you want forcast for
lon = 59
lat = 18

#Setting up API call function for SMHI forcast on location
#See https://opendata.smhi.se/apidocs/metfcst/parameters.html
smhi_url = "https://opendata-download-metfcst.smhi.se"
Sthlm_Lat = str(lon)
Sthlm_Lon = str(lat)
full_url = smhi_url+f"/api/category/pmp3g/version/2/geotype/point/lon/{Sthlm_Lon}/lat/{Sthlm_Lat}/data.json"
response = requests.get(full_url, verify=False)
status = response.raise_for_status()
data = response.json()

#Saving local file with indent to better analys json response.
with open("response.json","w") as f:
    f.write(json.dumps(data,indent=4))

#Finding position of values of interest: 
#According to docs, looking for name=ws, wd, gust and wsymb2

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
with open("localWindForcast.json","w") as f:
    f.write(json.dumps(weatherDict,indent=4))

#Conditional review of weatherdict to identify potential kitesurf dates
kitetimes = [time for time in weatherDict if weatherDict[time]["ws"] > 5 and weatherDict[time]["wd"] > 0 and weatherDict[time]["wd"] < 100]
[print(f"Lets KIIIITESURF at:   {time}") for time in kitetimes]