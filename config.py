import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 b'\xd5xB\x92\xf5\xa7\x1dP\xa2\x8f\xb8oi\xb4\x00\x1c'

    MONGODB_SETTINGS = {'db': 'UTA_Enrollment',
                        'host': 'mongodb://localhost:27017/UTA_Enrollment.study_flask'
                        }
