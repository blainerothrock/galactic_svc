import os

from flask import Flask
from flask_restful import Resource, Api

from utility import db

from services.echo import Echo
from services.auth import auth_bp
from services.game import game_bp

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)

api.add_resource(Echo, '/echo')

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

if __name__ == '__main__':
    app.run()
