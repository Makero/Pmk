from utils.msg import event
from utils.redis import redis


class MsgHandle:
    def __init__(self, dicts):
        self.reqData = dicts
        self.msg = event.MsgEvent(dicts)

    def type(self):
        """数据类型"""
        return self.reqData['MsgType[0]']

    def subscribe(self):
        """订阅"""
        event = self.reqData['Event[0]']
        userName = self.reqData['FromUserName[0]']
        if event == 'subscribe':
            print("用户 %s 关注成功"%(userName, ))
        elif event == 'unsubscribe':
            print("用户 %s 取消了关注"%(userName, ))

    def start(self):
        print(self.reqData)
        msgType = self.type()
        if msgType == 'event':
            self.subscribe()
        if msgType == 'voice':
            content = self.msg.data['Recognition']
        else:
            content = "成功啦！哈哈哈～😄"

        """
        msg.reply_news({
            'ArticleCount': 2,
            'Articles': {
                'item':[
                    {
                        'Title': '测试图文1',
                        'Description': '测试描述',
                        'PicUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/y1nlcyGpibk2qga7aTnYp2Ficdo6L174XdHGDFLevRseWibJ32eHdFIc3F85sIYib4J9JicjYnqqdZxTCWOeW4FZGdg/0?wx_fmt=jpeg',
                        'Url': 'https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1444738726'
                    },
                    {
                        'Title': '测试图文2',
                        'Description': '测试描述2',
                        'PicUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/y1nlcyGpibk2qga7aTnYp2Ficdo6L174XdHGDFLevRseWibJ32eHdFIc3F85sIYib4J9JicjYnqqdZxTCWOeW4FZGdg/0?wx_fmt=jpeg',
                        'Url': 'https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1444738726'
                    }
                ],
            }
        })
        """
        self.msg.reply_text(content)

        return {
            'code': 200,
            'data': self.msg.data
        }
