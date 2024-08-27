# from mongoengine import connect
# from mongoengine.errors import MongoEngineException


# def connection():

#     try:
#         connect(
#             db='DevOps',
#             host='mongodb',
#             port=27017,
#             username='devops',
#             password='devops007'
#             )
#     except MongoEngineException as exc:
#         print(f'Error={exc}')

from flask_mongoengine import MongoEngine

db = MongoEngine()


def init_db(app):
    db.init_app(app)
