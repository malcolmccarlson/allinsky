import bloomsky_api
import requests
import json
from configparser import ConfigParser


Config = ConfigParser()
Config.read('config.ini')

myapikey = Config.get('Authentication','BS_APIKEY')
myurl = Config.get('Authentication','DEFAULT_API_URL')

client = bloomsky_api.BloomSkyAPIClient(api_key=myapikey)
mydata = client.get_data()

def getbsdata():
    r = requests.get(myurl, headers={'Authorization': myapikey})
    converted = json.loads(r.text)
    return converted


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)

def getkeys():
    mydata = getbsdata()
    keylist = []
    for items in mydata:
        for key,value in recursive_items(items):
            keylist.append(key)
        print (keylist)

def getdata(mykey):
    mydata = getbsdata()
    for items in mydata:  #unpack the list of dictionaries
        for key, value in recursive_items(items): #search through the key value pares of the nested dicts for specific key
            if key == mykey:
                return (key,value)



if __name__ == '__main__':
    #getkeys()
    mytemp = getdata('Temperature')
    print (mytemp)

