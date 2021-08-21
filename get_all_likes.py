# -*- coding: utf-8 -*-
import configparser
import json
import datetime as dt
from requests_oauthlib import OAuth1Session

# read config
_config_file = configparser.ConfigParser()
_config_file.read('./config.ini')

# set oauth values
APK = _config_file.get('oauth', 'api_key')
APS = _config_file.get('oauth', 'api_secret')
ACT = _config_file.get('oauth', 'access_token') 
ACS = _config_file.get('oauth', 'access_secret')

# get user timeline 
_url = 'https://api.twitter.com/1.1/favorites/list.json'
#_url = 'https://api.twitter.com/2/users/:id/liked_tweets'
_twitter = OAuth1Session(APK, APS, ACT, ACS)
_req = _twitter.get(_url)
_my_tl = json.loads(_req.text)

# create all my tweeet list
_min_id = _my_tl[-1]['id']
while True:
    _params = {'max_id': _min_id - 1, 'count': 200}
    _req = _twitter.get(_url, params = _params)
    _tmp_tl = json.loads(_req.text)

    if len(_tmp_tl) == 0:
        break

    _min_id = _tmp_tl[-1]['id']
    _my_tl.extend(_tmp_tl)


# extract according to user config
TWITTER_DATE_FORMAT = _config_file.get('twitter', 'date_format')

for tweet in _my_tl:
    _create_date = dt.datetime.strptime(tweet['created_at'], TWITTER_DATE_FORMAT)
    print (_create_date.strftime('%Y/%m/%d') + ': ' + tweet['text'])
    
