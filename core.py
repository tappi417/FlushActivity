# -*- coding: utf-8 -*-

import ConfigParser
import json
import datetime as dt
from requests_oauthlib import OAuth1Session

# read config
_config_file = ConfigParser.SafeConfigParser()
_config_file.read('./config.ini')

CK = _config_file.get('oauth', 'consumer_key')
CS = _config_file.get('oauth', 'consumer_secret')
AT = _config_file.get('oauth', 'access_token') 
AS = _config_file.get('oauth', 'access_secret')

# get user timeline
_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json' 
_twitter = OAuth1Session(CK, CS, AT, AS)
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
DATE_FORMAT = _config_file.get('twitter', 'date_format')
PERIOD = dt.timedelta(days = int(_config_file.get('user', 'period')))
_period_date = dt.date.today() - PERIOD
_target_tweet = []
for tweet in _my_tl:
    _create_date = dt.datetime.strptime(tweet['created_at'], DATE_FORMAT)
    _create_date = dt.date(_create_date.year, _create_date.month, _create_date.day)
    if _create_date < _period_date:
        _target_tweet.append(tweet)

_destroy_url = 'https://api.twitter.com/1.1/statuses/destroy/:id.json'

# destroy target tweet without media
for tweet in _target_tweet:
    if 'media' not in tweet['entities']:
        _destroy_url = 'https://api.twitter.com/1.1/statuses/destroy/' + str(tweet['id']) + '.json'
        _req = _twitter.post(_destroy_url)
        print 'status: ' + str(_req.status_code)

