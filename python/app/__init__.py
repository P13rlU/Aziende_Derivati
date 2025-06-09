import os
from flask import Flask
from app.extensions import db, ma, swagger
from app.utils.json_encoder import CustomJSONProvider
from app.errors.handlers import register_error_handlers
from app.routes.dipendente_route import dipendenti_bp
from app.routes.cliente_route import clienti_bp
from app.routes.fattura_route import fatture_bp
from app.routes.prodotto_route import prodotti_bp
from app.routes.dettaglio_route import dettagli_bp
from app.routes.gestione_route import gestioni_bp
from app.routes.vendita_route import vendite_bp
from app.models import import_all_models
from app.logging_config import setup_logging

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    setup_logging(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    swagger.template_file = 'docs/swagger.yaml'
    swagger.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    app.json = CustomJSONProvider(app)
    register_error_handlers(app)

    with app.app_context():
        import_all_models()

    app.register_blueprint(dipendenti_bp)
    app.register_blueprint(clienti_bp)
    app.register_blueprint(fatture_bp)
    app.register_blueprint(prodotti_bp)
    app.register_blueprint(dettagli_bp)
    app.register_blueprint(gestioni_bp)
    app.register_blueprint(vendite_bp)

    return app

