from src.db import db
from src import create_app, config


app = create_app(config.Config)
with app.app_context():
    db.create_all()
