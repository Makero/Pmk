import time

class MsgEvent:
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