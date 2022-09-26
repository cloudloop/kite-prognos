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
Sthlm_Lat = "59.368718"
Sthlm_Lon = "18.200225"
full_url = smhi_url+f"/api/category/pmp3g/version/2/geotype/point/lon/{Sthlm_Lon}/lat/{Sthlm_Lat}/data.json"
response = requests.get(full_url, verify=False)
status = response.raise_for_status()
data = response.json()

#Saving local file with indent to better analys json response.
with open("response.json","w") as f:
    f.write(json.dumps(data,indent=4))

#Finding position of values of interest: 
#According to docs, looking for name=ws, wd, gust and wsymb2
#print(data["timeSeries"][i]["parameters[j]), where i = timeSeries and j = order for w/wd/gust etc
print(f'{data["timeSeries"][0]["parameters"][13]["name"]} {data["timeSeries"][0]["parameters"][13]["values"]}')
print(f'{data["timeSeries"][0]["parameters"][14]["name"]} {data["timeSeries"][0]["parameters"][14]["values"]}')
print(f'{data["timeSeries"][0]["parameters"][17]["name"]} {data["timeSeries"][0]["parameters"][17]["values"]}')
print(f'{data["timeSeries"][0]["parameters"][18]["name"]} {data["timeSeries"][0]["parameters"][18]["values"]}')
#j-values for our wanted values:
#wd: 13, ws: 14, gust: 17, wsymb2: 18

print(len(data["timeSeries"]))

weatherDict={}
for allTimes in range(len(data["timeSeries"])):
    print(allTimes)
    time = data["timeSeries"][allTimes]["validTime"]
    wd = data["timeSeries"][allTimes]["parameters"][13]["values"][0]
    ws = data["timeSeries"][allTimes]["parameters"][14]["values"][0]
    gust = data["timeSeries"][allTimes]["parameters"][17]["values"][0]
    wsymb2 = data["timeSeries"][allTimes]["parameters"][18]["values"][0]
    weatherDict[time] = {"wd": wd, "ws": ws, "gust": gust, "wsymb2": wsymb2}
print(json.dumps(weatherDict, indent=4))

