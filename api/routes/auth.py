from flask import Blueprint, request, g, session
from werkzeug.security import check_password_hash, generate_password_hash
from api.models.user import User, UserSchema
from api.utils.responses import response_with
import api.utils.responses as resp
from api.utils.database import db
import functools

bp_auth = Blueprint('auth_routes', __name__)


def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if g.user is not None:
            return f(*args, **kwargs)
        else:
            return response_with(resp.UNAUTHORIZED_403)

    return wrap


@bp_auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        user = user_schema.load(data)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={'user': result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@bp_auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password'], current_user.password):
            session.clear()
            session['user_id'] = current_user.id
            return response_with(resp.SUCCESS_201, value={'message': 'logged in as %s' % current_user.username})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@bp_auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return response_with(resp.SUCCESS_204)


@bp_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.find_by_id(user_id)
