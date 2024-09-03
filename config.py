import os

import mongomock


class DevConfig:

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USERNAME'),
        'password': os.getenv('MONGODB_PASSWORD')
    }


class ProdConfig:

    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_ATLAS_CONNECTION')
    }


class MockConfig:

    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'mongomock://localhost',
        'mongo_client_class': mongomock.MongoClient
    }
