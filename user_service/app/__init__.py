from flask import Flask
from .config import Config
from .models import db, ma
from .models import db, ma, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
