from flask import Flask
from flask_restful import Api

from .connection_db import init_db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    init_db(app)

    # Importa e registra as rotas
    from .routes import initialize_routes
    initialize_routes(app)

    return app
