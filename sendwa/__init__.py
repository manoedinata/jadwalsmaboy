from flask import Flask

from .database import db
from .database import migrate

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Routes
    from .routes import routes
    app.register_blueprint(routes)

    return app
