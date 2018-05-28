import json
from django.http import HttpResponse
from utils.api import wechat
from utils.redis import redis


def index(req):
    result = {'code': 404, 'data': {}}

    if req.method == 'GET' and req.GET:
        check = wechat.Validate()
        val = check.check_signature(req.GET)
        result['code'] = 200
        result['method'] = 'get'
        result['data']['bool'] = val

    if req.method == 'POST' and req.GET:
        result['code'] = 200
        result['method'] = 'post'

    return HttpResponse(json.dumps(result))


# def access(req):
#     rs = redis.Redis()
#     result = rs.get_redis(name="wechat", key="access_token")
#     return HttpResponse(result)


def handle(req):
    print(req.GET)
    if req.GET['MsgType[0]'] == 'voice':
        content = req.GET['Recognition[0]']
    else:
        content = "成功啦！哈哈哈～😄"

    msg = wechat.Message(req.GET)
    '''
    msg.reply_news({
        'ArticleCount': 1,
        'Articles': [
            {
                'Title': '测试图文',
                'Description': '测试描述',
                'PicUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/y1nlcyGpibk2qga7aTnYp2Ficdo6L174XdHGDFLevRseWibJ32eHdFIc3F85sIYib4J9JicjYnqqdZxTCWOeW4FZGdg/0?wx_fmt=jpeg',
                'Url': 'https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1444738726'
             }
        ],

    })
    '''
# msg.reply_text(content)
    msg.reply_image('LCBbOH4e-Pa68zj-4KqCCPf1j_XEHlBT5y50my8HBVJcfEfDeiID0YDyvBI3VpGT')
    data = {
        'code': 200,
        'data': msg.data
    }
    print(data)
    return HttpResponse(json.dumps(data))


def page_not_found(req):

    data = {'code': 404, 'data': {}}
    return HttpResponse(json.dumps(data))
