import os
from flask import Flask
from flask import jsonify

from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.config.config import *

from api.routes.auth import bp_auth

from api.models import *

app = Flask(__name__)

if os.environ.get('ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('ENV') == 'DEV':
    app_config = DevelopmentConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)


@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    app.logger.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    app.logger.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    app.logger.error(e)
    return response_with(resp.SERVER_ERROR_404)


@app.errorhandler(404)
def not_found(e):
    app.logger.error(e)
    return response_with(resp.SERVER_ERROR_404)


db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(bp_auth, url_prefix='/api/auth')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', use_reloader=False)
