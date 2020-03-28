from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_restful import (
    Api, Resource, reqparse, fields, marshal_with
)

import numpy as np

from services.auth import login_required
from utility.db import get_db

game_bp = Blueprint('game', __name__, url_prefix='/game')
api = Api(game_bp)

class Create(Resource):
    @login_required
    def get(self):
        l = list(np.random.rand(3, 2))
        return { 'alive': True, 'message': 'hello %s' % g.user['name'], 'list': l }, 200

api.add_resource(Create, '/create')