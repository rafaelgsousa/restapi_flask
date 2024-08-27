from flask import Flask

from .connection_db import init_db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    init_db(app)

    # Importa e registra as rotas
    from .controller import initialize_routes
    initialize_routes(app)

    return app
