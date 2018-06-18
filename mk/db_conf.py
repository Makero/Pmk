ENV = 'localhost'

DB = {

    'family': {
        'mysql': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '192.168.0.200',
            'NAME': 'mk_wechat_db',
            'USER': 'root',
            'PASSWORD': 'maker',
            'PORT': '3306',
        },
        'redis': {
            'host': '192.168.0.200',
            'password': '2018maker',
            'port': 6379,
            'db': 0,
        }
    },

    'localhost': {
        'mysql': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'NAME': 'mk_wechat_db',
            'USER': 'root',
            'PASSWORD': 'maker',
            'PORT': '3306',
        },
        'redis': {
            'host': 'localhost',
            'password': '',
            'port': 6379,
            'db': 0,
        }
    },

    'aliyun': {
        'mysql': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '47.93.198.225',
            'NAME': 'mk_wechat_db',
            'USER': 'root',
            'PASSWORD': 'Maker123',
            'PORT': '3306',
        },
        'redis': {
            'host': '47.93.198.225',
            'password': '2018maker<&>',
            'port': 6379,
            'db': 0,
        }
    }

}
