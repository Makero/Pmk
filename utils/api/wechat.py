###########################
#
# 微信API调用的方法
#
###########################
import hashlib
import time
from utils.api import wechat_conf as wx
from utils.request import request as req


class Validate:
    """验证类"""
    def __init__(self):
        self.token = wx.TOKEN
        self.signature = None
        self.bool = False

    def get_signature(self, timestamp, nonce):
        """获取token加密签名"""
        tmp = [self.token, timestamp, nonce]
        tmp.sort()
        _str = ''.join(tmp).encode(encoding='UTF-8')
        self.signature = hashlib.sha1(_str).hexdigest()

    def check_signature(self, param):
        """检测token加密签名是否正确"""
        self.get_signature(param.get('timestamp'), param.get('nonce'))

        if self.signature == param.get('signature'):
            self.bool = True

        return self.bool


class AccessToken:
    """获取access_token类"""
    def __init__(self):
        self.url = wx.API_URL['access_token']
        self.data = {
            'grant_type': 'client_credential',
            'appid': wx.APP_ID,
            'secret': wx.APP_SECRET,
        }

    def get(self):
        """获取access_token"""
        result = req.get_api({
            'url': self.url,
            'data': self.data,
        })
        return result


class Message:
    def __init__(self, dicts):
        self.data = {
            'ToUserName': dicts['FromUserName[0]'],
            'FromUserName': dicts['ToUserName[0]'],
            'CreateTime': int(time.time()),
            'MsgType': None
        }

    def reply_text(self, content):
        self.data['MsgType'] = 'text'
        self.data['Content'] = content

    def reply_image(self, media_id):
        self.data['MsgType'] = 'image'
        self.data['MediaId'] = media_id

    def reply_voice(self, media_id):
        self.data['MsgType'] = 'voice'
        self.data['MediaId'] = media_id

    def reply_video(self, media_id, title=None, description=None):
        self.data['MsgType'] = 'video'
        self.data['MediaId'] = media_id
        self.data['Title'] = title
        self.data['Description'] = description

    def reply_music(self, thumb_media_id, title=None, description=None, music_url=None, hq_music_url=None):
        self.data['MsgType'] = 'music'
        self.data['Title'] = title
        self.data['Description'] = description
        self.data['MusicURL'] = music_url
        self.data['HQMusicUrl'] = hq_music_url
        self.data['ThumbMediaId'] = thumb_media_id

    def reply_news(self, dicts):
        """
        dicts数据格式
        dicts = {
            'ArticleCount': 2,
            'Articles': {
                'item':[
                    {
                        'Title': title,
                        'Description': description,
                        'PicUrl': pic_url,
                        'Url': url
                    },
                    {
                        'Title': title,
                        'Description': description,
                        'PicUrl': pic_url,
                        'Url': url
                    }
                ],
            }
        } 
        """
        self.data['MsgType'] = 'news'
        self.data['ArticleCount'] = dicts['ArticleCount']
        self.data['Articles'] = dicts['Articles']
