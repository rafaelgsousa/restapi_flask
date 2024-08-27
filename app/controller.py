from flask import jsonify
from mongoengine import ValidationError
from mongoengine.errors import MongoEngineException

import app

from .models import User
from .parses import parser_user


def initialize_routes(api):
    @api.route("/", methods=['GET'])
    def get_hello():
        return {'hello': 'world'}

    @api.route("/devops", methods=['POST'])
    def post_dev():
        try:
            data = parser_user.parse_args()
            dev = User(**data)
            dev.save()
            return jsonify({'message': dev.name}), 201
        except ValidationError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        except MongoEngineException as exc:
            return handle_exception(exc, "Error saving user data", 500)

    @api.route("/devops/<string:cpf>", methods=['GET'])
    def get_dev(cpf):
        try:
            devs = User.objects(cpf=cpf)

            if not devs:
                return {'message': 'User not found'}, 404
            user_data = [
                {
                    'name': dev.name,
                    'id': str(dev.id),
                    'nickname': dev.nickname,
                    'age': dev.age,
                    'email': dev.email,
                    'cpf': dev.cpf,
                    'self_image': dev.self_image if dev.self_image else ''
                } for dev in devs
            ]
            return jsonify(user_data)
        except User.DoesNotExist as exc:
            return handle_exception(exc, "User not found", 404)
        except MongoEngineException as exc:
            return handle_exception(exc, "Error fetching user data", 500)

    def handle_exception(error, message, status_code):
        # Logar a exceção completa para análise posterior
        app.logger.error(f"Error: {error}")

        # Retornar uma mensagem personalizada para o usuário
        return jsonify({'error': message}), status_code
