def create_random_string(digit):
    """ 随机生成一串字符串 长度为digit """
    import random
    s = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    return ''.join([random.choice(s) for _ in range(digit)])


def create_token(username):
    """ 生成token """
    import time
    import hashlib
    _hash = hashlib.md5(str(time.time()).encode(encoding='utf-8'))
    _hash.update(username.encode(encoding='utf-8'))
    return _hash.hexdigest()
