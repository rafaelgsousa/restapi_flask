import mimetypes
import os
import uuid

from flask import jsonify, make_response, request, send_from_directory
from mongoengine import ValidationError
from mongoengine.errors import MongoEngineException
from werkzeug.utils import secure_filename

import app
from utils import check_image, check_pdf

from .models import User
from .parses import parser_user

UPLOAD_FOLDER = 'media'


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
            return _handle_exception(exc, "Error saving user data", 500)

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
            return _handle_exception(exc, "User not found", 404)
        except MongoEngineException as exc:
            return _handle_exception(exc, "Error fetching user data", 500)
        
    @api.route("/devops/change/selfimage", methods=['PATCH'])
    def change_selfimage():
        if 'id' not in request.form or 'file' not in request.files:
            return jsonify({'error': 'Bad Request'}), 401
        id = request.form['id']
        file_send = request.files['file']
        filename = secure_filename(file_send.filename)
        if not check_image(filename):
            return jsonify({'error': 'Bad Request'}), 401
        if not os.path.exists(f'{UPLOAD_FOLDER}/{id}'):
            os.makedirs(f'{UPLOAD_FOLDER}/{id}')
        relpath = os.path.join(f'{UPLOAD_FOLDER}/{id}', filename)
        user = User.objects(id=id)
        user.update(set__self_image=os.getenv('URL') + '/devops/download/file?' + f'id={id}&file={filename}')
        file_send.save(relpath)
        return jsonify({'message': f'File saved with name {filename} successfully'}), 201

        
    @api.route("/devops/upload/file", methods=['POST'])
    def upload_file():
        if 'id' not in request.form or 'file' not in request.files:
            return jsonify({'error': 'Bad Request'}), 401
        id = request.form['id']
        file_send = request.files['file']
        filename = secure_filename(file_send.filename)
        if not check_pdf(filename):
            return jsonify({'error': 'Bad Request'}), 401
        if not os.path.exists(f'{UPLOAD_FOLDER}/{id}'):
            os.makedirs(f'{UPLOAD_FOLDER}/{id}')
        relpath = os.path.join(f'{UPLOAD_FOLDER}/{id}', filename)
        file_send.save(relpath)
        return jsonify({'message': f'File saved with name {filename} successfully'}), 201


    @api.route('/devops/download/file', methods=['GET'])
    def download_file():
        filename = request.args.get('file')
        user_id = request.args.get('id')

        if not filename or not user_id:
            return jsonify({'error': 'Missing parameters'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, user_id, filename)
        absfilepath = os.path.abspath(filepath)
        if not os.path.exists(absfilepath):
            return jsonify({'error': 'File not found'}), 404

        # try:
        #     return send_from_directory(os.path.dirname(absfilepath), filename, as_attachment=True)
        # except Exception as e:
        #     return jsonify({'error': str(e)}), 500
        try:
            with open(absfilepath, 'rb') as f:
                file_content = f.read()
                content_type = mimetypes.guess_type(absfilepath)[0] or 'application/octet-stream'
                response = make_response(file_content)
                response.headers['Content-Type'] = content_type
                response.headers['Content-Disposition'] = 'inline; filename={}'.format(filename)
                return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def _handle_exception(error, message, status_code):
        # Logar a exceção completa para análise posterior
        app.logger.error(f"Error: {error}")

        # Retornar uma mensagem personalizada para o usuário
        return jsonify({'error': message}), status_code
