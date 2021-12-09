import requests 
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://10.1.70.17/abx/api"

#login and get a token
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
response = requests.request("POST", url + "/login", headers=headers, json= {"username": "ABXAdmin","password": "temPassw0rd123$","isEulaConfirmed": "true"}, verify=False)
token = response.json()["token"]

#create a list of the pictures' names
pictures = []
for i in os.listdir():
    if "jpg" in i or "png" in i:
        pictures.append(i)

#feature extraction from pic + create member
headers = {
    "Authorization": "bearer {}".format(token),
    "Accept": "application/json"
}
for filename in pictures:
    with open(filename, 'rb') as file:
        #the requests.request() function's kwarg "files" takes a dictionary of {'name': file-like-objects} for uploading a file 
        files = {"file": file}
        response = requests.request("POST", url + "/image/extract", headers=headers, files=files, verify=False).json()
        features = response["items"][0]["crops"][0]["features"]
        path = response["items"][0]["crops"][0]["backup"]["path"]
        payload = {
            "name": filename.split(".")[0],
            "images": [{
                "objectType": 1,
                "featuresQuality": 0,
                "url": path,
                "features": features
                }]
        }
        response = requests.request("POST", url + "/members", headers=headers, json=payload, verify=False)
    

    


