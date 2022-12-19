# importing the requests library
import requests

json = {'message':'testing logging to dbs'}

def log_to_api(json):    
    # localhost
    API_ENDPOINT = "http://127.0.0.1:8000/log"

    # remote
    # API_ENDPOINT = "https://sea-turtle-app-fwxog.ondigitalocean.app/log"
    
    # Sending a post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, json = json)

    # extracting response text 
    return r

r = log_to_api(json)
print(r.text)