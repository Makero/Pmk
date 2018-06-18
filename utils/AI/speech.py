from aip import AipSpeech


class Speech:
    def __init__(self):
        """ 你的 APPID AK SK """
        self.app_id = '9005055'
        self.api_key = 'EZBl2T4NwCs2TyADthxwCnNz'
        self.secret_key = 'd0619836d8fa970fe330e823d64b3318'
        self.client = AipSpeech(self.app_id, self.api_key, self.secret_key)

    def synthesis(self, talk):
        return self.client.synthesis(talk, 'zh', 1, {'vol': 5, 'per': 4})
