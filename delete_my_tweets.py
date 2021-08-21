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
_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json' 
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
PERIOD_DATE_YEAR = int(_config_file.get('period', 'year'))
PERIOD_DATE_MONTH = int(_config_file.get('period', 'month'))
PERIOD_DATE_DAY = int(_config_file.get('period', 'day'))
_period_date = dt.date(PERIOD_DATE_YEAR, PERIOD_DATE_MONTH, PERIOD_DATE_DAY)

_target_tweet = []
for tweet in _my_tl:
    _create_date = dt.datetime.strptime(tweet['created_at'], TWITTER_DATE_FORMAT)
    _create_date = dt.date(_create_date.year, _create_date.month, _create_date.day)
    if _create_date < _period_date:
        _target_tweet.append(tweet)

# destroy target tweet without media
for tweet in _target_tweet:
    _destroy_url = 'https://api.twitter.com/1.1/statuses/destroy/' + str(tweet['id']) + '.json'
    _req = _twitter.post(_destroy_url)
    
    _create_date = dt.datetime.strptime(tweet['created_at'], TWITTER_DATE_FORMAT)
    _create_date = dt.date(_create_date.year, _create_date.month, _create_date.day)
    print ('status: ' + str(_req.status_code))
    print (_create_date.strftime('%Y/%m/%d') + ': ' + tweet['text'])

