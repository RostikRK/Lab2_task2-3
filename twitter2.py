import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import requests
import pprint

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
def get_friends_file():
    cyc_val = True
    while cyc_val == True:
        print('')
        acct = input('Enter Twitter Account: ')
        if len(acct) < 1:
            break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '10'})
        #connection = urllib.request.urlopen(url, context=ctx)
        #data = connection.read().decode()
        #print(data[:250])
        #headers = dict(connection.getheaders())
        # print headers
        #print('Remaining', headers['x-rate-limit-remaining'])
        responce = requests.get(url)
        data = responce.json()
        with open("friends.json", "w", encoding='utf-8') as fille:
            json.dump(data, fille, indent=4)
        print("Change the user? (Y/N). If no we will start navigation with this user timeline.")
        ans = input()
        while True:
            if ans == "N":
                cyc_val = False
                break
            elif ans == "Y":
                break
            else:
                ans = input("Wrong input. Please try again.(Y/N): ")