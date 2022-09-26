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
print(status)
with open("response.json","w") as f:
    data = response.json()
    f.write(json.dumps(data, indent=4))

with open("response.json","r") as f:
    g = f.read()
    h = json.dumps(g)
    i = h["timeSeries"]
    print(type(h))



