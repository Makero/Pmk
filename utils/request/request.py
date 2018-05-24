import ssl
import json
import urllib.request as request
import urllib.parse as parse


def get_api(params):
    data = parse.urlencode(params['data'])
    url = params['url'] + "?" + data
    context = ssl._create_unverified_context()
    result = request.urlopen(url, context=context).read().decode('utf-8')
    return json.loads(result)


def post_api(params):
    pass
