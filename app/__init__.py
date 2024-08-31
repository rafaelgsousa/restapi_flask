from flask import Flask

from .connection_db import init_db

UPLOAD_FOLDER = 'media'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    init_db(app)

    # Importa e registra as rotas
    from .controller import initialize_routes
    initialize_routes(app)

    return app
