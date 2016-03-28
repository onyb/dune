import os


class _Config(object):
    DEBUG = True
    TESTING = False

    ROOT_DIR = '/home/ani' #os.environ['HOME']
    ASSETS_DIR = os.path.join(ROOT_DIR, 'dune_assets')



class Prod(_Config):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'host': 'mongodb://USERNAME:PASSWORD@HOST',
    }


class Dev(_Config):
    NAME = "Dev"
    DEBUG = True
    MONGO_DBNAME = 'dune'


class Testing(_Config):
    NAME = "Test"
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test_db'
    }
