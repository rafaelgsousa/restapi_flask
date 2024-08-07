from flask import jsonify, request
from mongoengine.errors import MongoEngineException

from .models import User


def initialize_routes(api):
    @api.route("/", methods=['GET'])
    def get_hello():
        return {'hello': 'world'}

    @api.route("/devops", methods=['POST'])
    def post_dev():
        try:
            data = request.get_json()
            dev = User(**data)
            dev.save()
            return jsonify({'message': dev.name}), 201
        except MongoEngineException as exc:
            print(f'Error={exc}')
            return jsonify({'error': str(exc)}), 500

    @api.route("/devops/<string:name>", methods=['GET'])
    def get_dev(name):
        try:
            devs = User.objects(name=name)
            user_data = [
                {
                    'name': dev.name,
                    'id': str(dev.id),
                    'nickname': dev.nickname,
                    'age': dev.age,
                    'email': dev.email,
                    'self_image': dev.self_image if dev.self_image else ''
                } for dev in devs
            ]
            return jsonify(user_data)
        except User.DoesNotExist:
            return jsonify({'error': 'Not found'}), 404
        except MongoEngineException as exc:
            print(f'Error={exc}')
            return jsonify({'error': str(exc)}), 500
