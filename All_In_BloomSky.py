import bloomsky_api
import requests
import json
from configparser import ConfigParser
import argparse

Config = ConfigParser()
Config.read('config.ini')

myapikey = Config.get('Authentication', 'BS_APIKEY')
myurl = Config.get('Authentication', 'DEFAULT_API_URL')

client = bloomsky_api.BloomSkyAPIClient(api_key=myapikey)
mydata = client.get_data()


parser = argparse.ArgumentParser(description='Access BloomSky weather data')
parser.add_argument('-s', '--showkeys', action='store_true', default=False,
                    help='Prints a list of keys')
parser.add_argument('-k', '--key', metavar='', required=False,
                    help='Passes key in and gets value.')
args = parser.parse_args()


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
    keydata = getbsdata()
    keylist = []
    for items in keydata:
        for key, value in recursive_items(items):
            keylist.append(key)
        return keylist


def getdata(mykey):
    mydat = getbsdata()
    for items in mydat:
        for key, value in recursive_items(items):
            if key == mykey:
                keyval = (key, value)
                return keyval


if __name__ == '__main__':

    if args.showkeys:
        print(getkeys())
    else:
        bsinfo = getdata(args.key)
        print(bsinfo)
