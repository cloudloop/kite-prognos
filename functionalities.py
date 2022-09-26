#Functionalities
import json
with open("response.json","r") as f:
    data = json.loads(f.read())
    print(type(data))
    d2= data["timeSeries"]["parameters"]
    print(d2)