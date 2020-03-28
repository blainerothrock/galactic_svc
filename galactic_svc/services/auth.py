import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_restful import (
    Api, Resource, reqparse, fields, marshal_with
)
from werkzeug.security import check_password_hash, generate_password_hash

from utility.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(auth_bp)


def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if g.user is not None:
            return f(*args, **kwargs)
        else:
            return { 'error': 'login is required' }, 401

    return wrap


register_parser = reqparse.RequestParser()
register_parser.add_argument(
    'username',
    type=str,
    help='username is required',
    required=True,
    location='json'
)
register_parser.add_argument(
    'password',
    type=str,
    location='json',
    required=True,
    help='password is required'
)
register_parser.add_argument(
    'name',
    type=str,
    location='json',
    required=True,
    help='name is required'
)


class Register(Resource):
    def post(self, **kwargs):
        args = register_parser.parse_args()
        username = args['username']
        password = args['password']
        name = args['name']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User %s is already registered' % username

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, name) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), name)
            )
            db.commit()
        else:
            return {
                       'success': False,
                       'error': error
                   }, 400

        return {
            'success': True
        }

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'username',
    type=str,
    help='username is required',
    required=True,
    location='json'
)
login_parser.add_argument(
    'password',
    type=str,
    location='json',
    required=True,
    help='password is required'
)


class Login(Resource):
    def post(self, **kwargs):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Auth Failure'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return {
                'success': True
            }
        else:
            return {
               'success': False,
               'error': error
            }, 403

class Logout(Resource):
    def post(self):
        session.clear()
        return '', 201

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()
