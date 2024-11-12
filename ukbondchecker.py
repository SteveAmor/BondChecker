import requests
import json
import os.path
import os
from datetime import datetime

ThisMonthsFile = '/dev/shm/sample.json'
HolderNumber = '123456789'

def isThisMonthsFileAWin():
    if not (os.path.exists(ThisMonthsFile)):
        return False # File doesn't exist
    try:
        with open(ThisMonthsFile, 'r') as openfile:
            json_object = json.load(openfile)
    except:
        return False # JSON is missing or corrupt

    if 'status' not in json_object:
       return False # JSON should at the very least have a status key

    return (isThisMonthsFile(json_object)) # JSON

def isThisMonthsFile(json_object):
    monthYear = datetime.now().strftime("%B %Y") # eg 'September 2024'
    try:
        if HolderNumber not in (json_object['holder_number']):
            return False # JSON is not for current holder number
    except:
        return False # 'holder_number' key is missing from JSON
    try:
        if monthYear in (json_object['history'][0]['date']):
            return True # JSON says we have won this month
    except:
        return False # 'history' key missing from JSON
    return False # JSON suggests we haven't won this month



if(isThisMonthsFileAWin()):

    print("We have already notified a win this month")
    exit(0)

print("Getting premium bonds data for holder", HolderNumber)

url = "https://www.nsandi.com/premium-bonds-have-i-won-ajax"
payload = {
    "field_premium_bond_period": "this_month",
    "field_premium_bond_number": HolderNumber
}

response = requests.post(url, data=payload, timeout=5)

response_data = response.json()

if (response_data['status'] == 'win' and isThisMonthsFile(response_data)):
    message = response_data['tagline']
    os.system("python /home/pi/emailsubject.py \"%s\""%message) # Replace with your method of notification

print(response_data['header'], response_data['tagline'])

with open(ThisMonthsFile, "w") as outfile:
    outfile.write(response.text)

