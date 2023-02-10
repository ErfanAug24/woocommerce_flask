from src.db import db
from src import create_app, config


app = create_app(config.Config)
with app.app_context():
    db.init_app(app)
    db.create_all()
