from flask import Flask
from flask_restful import Api

from .connection_db import connection


def create_app():
    connection()
    app = Flask(__name__)
    api = Api(app)

    # Importa e registra as rotas
    from .routes import initialize_routes
    initialize_routes(app)

    return app
