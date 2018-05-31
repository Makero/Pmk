import time
from utils.msg import event
from utils.redis import redis
from wechat import models


class MsgHandle:
    def __init__(self, dicts):
        print(dicts)
        self.reqData = dicts
        self.msg = event.MsgEvent(dicts)

        self.msgType = dicts['MsgType[0]']
        self.eventType = None
        self.userName = dicts['FromUserName[0]']
        self.createDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(dicts['CreateTime[0]'])))

    def __subscribe(self):
        """订阅"""
        subscriber = models.Subscriber.objects
        operation = models.Operation.objects
        s_filter = subscriber.filter(openid=self.userName)

        if self.eventType == 'subscribe':
            if s_filter:
                s_filter.update(status='S')
                operation.create(subscriber_id=s_filter[0].id, date=self.createDate, status='S')
            else:
                user = subscriber.create(openid=self.userName, status='S')
                operation.create(subscriber_id=user.id, date=self.createDate, status='S')
        elif self.eventType == 'unsubscribe':
            s_filter.update(status='U')
            operation.create(subscriber_id=s_filter[0].id, date=self.createDate, status='U')

    def __voice(self):
        return self.reqData['Recognition[0]']

    def start(self):
        """消息处理"""
        if self.msgType == 'event':
            self.eventType = self.reqData['Event[0]']
            self.__subscribe()
        if self.msgType == 'voice':
            content = self.__voice()
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
