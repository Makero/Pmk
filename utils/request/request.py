import json
import requests
from urllib import parse


def get_api(params):
    data = parse.urlencode(params['data'])
    if len(data):
        url = params['url'] + "?" + data
    else:
        url = params['url']
    try:
        result = requests.get(url=url, json=params['data'])
    except:
        return json.loads('{"content": "网络不可用，API调用失败啦～"}')
    return json.loads(result.text)


def post_api(params):
    data = parse.urlencode(params['data'])
    if len(data):
        url = params['url'] + "?" + data
    else:
        url = params['url']
    try:
        result = requests.get(url=url, json=params['data'])
    except:
        return json.loads('{"content": "网络不可用，API调用失败啦～"}')
    return json.loads(result.text)
