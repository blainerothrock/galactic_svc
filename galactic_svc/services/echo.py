from flask import Flask
from flask_restful import Resource, reqparse, fields, marshal_with

parser = reqparse.RequestParser()
parser.add_argument(
    'message',
    type=str,
    help='Message cannot be blank',
    required=True,
    location='json'
)
parser.add_argument(
    'list',
    action='append',
    type=int,
    location='json'
)

resource_fields = {
    'message': fields.String,
    'list': fields.List(fields.Integer)
}


class Echo(Resource):
    @marshal_with(resource_fields, envelope="res")
    def post(self, **kwargs):
        args = parser.parse_args()
        return {
            'message': args['message'],
           'list': args['list']
        }, 200