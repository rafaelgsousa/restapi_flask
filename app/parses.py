from flask_restful import reqparse
from mongoengine import ImageField

parser_user = reqparse.RequestParser()
parser_user.add_argument(
                        'name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

parser_user.add_argument(
                        'nickname',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
parser_user.add_argument(
                        'age',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )
parser_user.add_argument(
                        'email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
parser_user.add_argument(
                        'cpf',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
parser_user.add_argument(
                        'self_image',
                        type=ImageField,
                        required=False,
                        help="This field cannot be blank."
                        )
