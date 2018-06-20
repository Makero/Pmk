import time
from utils.msg import event
from wechat import models
from utils.AI import chat
from utils.request import request as req
from utils.redis import redis
from wechat import prompt_conf as pr


class Search:
    def __init__(self, name=None):
        self.name = name
        self.api_url = 'http://tingapi.ting.baidu.com/v1/restserver/ting'

    def music_list(self, msg):

        result = req.get_api({
            'url': self.api_url,
            'data': {
                'method': 'baidu.ting.search.catalogSug',
                'query': self.name
            }
        })
        try:
            err = result['errno']
        except KeyError:
            err = False

        if err:
            msg.reply_text(pr.MUSIC_NONE)
        else:
            id = result['song'][0]['songid']
            msg.reply_news({
                'ArticleCount': 1,
                'Articles': {
                    'item': [
                        {
                            'Title': result['song'][0]['songname'],
                            'Description': '点我进入音乐播放界面',
                            'PicUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/y1nlcyGpibk2qga7aTnYp2Ficdo6L174XdHGDFLevRseWibJ32eHdFIc3F85sIYib4J9JicjYnqqdZxTCWOeW4FZGdg/0?wx_fmt=jpeg',
                            'Url': 'http://www.20mk.cn/music?songid='+id
                        }
                    ],
                }
            })

    def music_play(self, song_id):

        result = req.get_api({
            'url': self.api_url,
            'data': {
                'method': 'baidu.ting.song.play',
                'songid': song_id
            }
        })
        return result

    def music_lrc(self, song_id):

        result = req.get_api({
            'url': self.api_url,
            'data': {
                'method': 'baidu.ting.song.lry',
                'songid': song_id
            }
        })
        return result


class MsgHandle:
    def __init__(self, dicts):
        self.robot = chat.ChatRobot()
        self.reqData = dicts
        self.msg = event.MsgEvent(dicts)

        self.msgType = dicts['MsgType[0]']
        self.eventType = None
        self.userName = dicts['FromUserName[0]']
        self.createDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(dicts['CreateTime[0]'])))

    def __subscribe(self):
        """订阅与退阅事件处理"""
        subscriber = models.Subscriber.objects
        operation = models.Operation.objects
        s_filter = subscriber.filter(openid=self.userName)

        if self.eventType == 'subscribe':
            if s_filter:
                s_filter.update(status='S')
                operation.create(subscriber_id=s_filter[0].id, date=self.createDate, status='S')
                self.msg.reply_text(pr.WELCOME_AGAIN)
            else:
                user = subscriber.create(openid=self.userName, status='S')
                operation.create(subscriber_id=user.id, date=self.createDate, status='S')
                self.msg.reply_text(pr.WELCOME_FIRST)

        elif self.eventType == 'unsubscribe':
            s_filter.update(status='U')
            operation.create(subscriber_id=s_filter[0].id, date=self.createDate, status='U')

    def __match(self, content):
        rs = redis.Redis()
        if content == "1000":
            self.msg.reply_news(pr.INSTRUCTIONS)
        elif content == "1001" or content == "一千零一":
            rs.set_redis(name='message', key=self.userName, value='music')
            self.msg.reply_text(pr.MUSIC_FUNC_START)
        elif content == "1002" or content == "一千零二":
            rs.set_redis(name='message', key=self.userName, value='text')
            self.msg.reply_text(pr.MUSIC_FUNC_STOP)
        else:
            val = rs.get_redis(name='message', key=self.userName)
            if val is None:
                mess_type = 'text'
            else:
                mess_type = val.decode(encoding='UTF-8')
            if mess_type == 'music':
                Search(content).music_list(self.msg)
            else:
                result = self.robot.inter_locution(content)
                self.msg.reply_text(result['data']['text'].replace('/n', '\n'))

    def __text(self):
        """文本消息处理"""
        content = self.reqData['Content[0]']
        self.__match(content)

    def __voice(self):
        """语音消息处理"""
        recognition = self.reqData['Recognition[0]']
        content = recognition[0:len(recognition)-1]
        self.__match(content)

    def __image(self):
        """图片消息处理"""
        pass

    def __location(self):
        """地理位置消息处理"""
        pass

    def __link(self):
        """链接消息处理"""
        pass

    def __file(self):
        """文件消息处理"""
        pass

    def start(self):
        """消息处理开始"""
        if self.msgType == 'event':
            self.eventType = self.reqData['Event[0]']
            self.__subscribe()
        elif self.msgType == 'text':
            self.__text()
        elif self.msgType == 'voice':
            self.__voice()
        elif self.msgType == 'image':
            self.__image()
        elif self.msgType == 'location':
            self.__location()
        elif self.msgType == 'file':
            self.__file()
        else:
            content = "这是什么，😄哈哈哈～"

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

        return {
            'code': 200,
            'data': self.msg.data
        }
