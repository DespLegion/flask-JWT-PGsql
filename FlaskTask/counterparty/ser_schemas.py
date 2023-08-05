from flask_restx import Model
from flask_restx.fields import String, Integer
from flask_restx import reqparse
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser


comp_reqparser = RequestParser(bundle_errors=True)
comp_reqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
# comp_reqparser.add_argument(
#     name="password", type=str, location="form", required=True, nullable=False
# )
#
# custom_greeting_parser.add_argument('greeting', required=True, location='json')

custom_greeting_parser = reqparse.RequestParser()
# custom_greeting_parser.add_argument('greeting', required=True, location='json')

counterparty_fields = Model(
    "counterparty",
    {
        'id': Integer,
        'sysName': String,
        'name': String,
        'setDate': Integer,
    },
)
