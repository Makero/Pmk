import ssl
import urllib.request as request
import urllib.parse as parse


def api_get(params):
    data = parse.urlencode(params['data'])
    url = params['url'] + "?" + data
    context = ssl._create_unverified_context()
    result = request.urlopen(url, context=context).read().decode('utf-8')
    return result


def api_post(params):
    pass
