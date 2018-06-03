import json
import requests
from urllib import parse


def get_api(params):
    data = parse.urlencode(params['data'])
    if len(data):
        url = params['url'] + "?" + data
    else:
        url = params['url']
    result = requests.get(url=url, json=params['data'])
    return json.loads(result.text)


def post_api(params):
    data = parse.urlencode(params['data'])
    if len(data):
        url = params['url'] + "?" + data
    else:
        url = params['url']
    result = requests.post(url=url, json=params['data'])
    return json.loads(result.text)
