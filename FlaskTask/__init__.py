from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required
from config import Config
from flask import Blueprint
from flask_restx import Api, fields, Namespace, Resource, reqparse
from .models import db
from http import HTTPStatus


app = Flask(__name__)
app.config.from_object(Config)


from .models.user import User
from .models.c_models import Company, Counterparty

# from .ser.cont_sc import counterparties_ns, counterparty_fields
from FlaskTask.user.endpoints import auth_ns
from FlaskTask.counterparty.endpoints import counterparty_ns


jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api = Api(
    api_bp,
    version='1.0',
    title='flask task API',
    description='Welcome to the Swagger UI documentation site!',
    doc='/swagger',
    authorizations=authorizations,
)

app.register_blueprint(api_bp)
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(counterparty_ns, path="/counterparties")

# resource_fields = api.model('Resource', {
#     'name': fields.String,
# })
#
# auth_user = Namespace(name="auth", validate=True)
# # api.add_namespace(auth_user)
#
# @auth_user.route('/register', methods=['POST'])
# # @api.marshal_with(resource_fields)
# @auth_user.expect(auth_reqparser)
# @auth_user.response(int(HTTPStatus.CREATED), "New user was successfully created.")
# @auth_user.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
# @auth_user.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
# def register():
#     params = request.json
#     user = User(**params)
#     db.session.add(user)
#     db.session.commit()
#     token = user.get_token()
#     return {'access_token': token}


# auth_ns = Namespace(name="auth", validate=True)
# api.add_namespace(auth_ns, path="/auth")
# custom_greeting_model = auth_ns.model('Custom', {
#     'greeting': fields.String(required=True),
#     'id': fields.Integer(required=True),
# })
custom_greeting_parser = reqparse.RequestParser()
custom_greeting_parser.add_argument('greeting', required=True, location='json')


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.auth(**params)
    token = user.get_token()
    return {'access_token': token}


# api.add_namespace(counterparties_ns, path="/counterparties")


# @counterparties_ns.route('/api/v1/counterparties', methods=['GET'])
# # @jwt_required()
# class GetCounterparties(Resource):
#     @api.marshal_list_with(counterparty_fields)
#     def api_counterparties_get_list(self):
#         counterparties = Counterparty.query.all()
#         serialized = []
#         for counterparty in counterparties:
#             serialized.append({
#                 'name': counterparty.name
#             })
#         return jsonify(serialized)


@app.route('/api/v1/counterparties', methods=['POST'])
@jwt_required()
def api_counterparties_new_list():
    new_list = Counterparty(**request.json)
    db.session.add(new_list)
    db.session.commit()
    serialized = {
        'id': new_list.id,
        'sysName': new_list.sysName,
        'name': new_list.name,
        'setDate': new_list.setDate
    }
    return jsonify(serialized)


@app.route('/api/v1/counterparties/<int:counterparty_id>', methods=['GET'])
@jwt_required()
def api_counterparty_get(counterparty_id):
    counterparty = Counterparty.query.filter(Counterparty.id == counterparty_id).first()
    if not counterparty:
        return {'message': 'No counterparty with this ID'}, 400
    serialized = {
        'id': counterparty.id,
        'sysName': counterparty.sysName,
        'name': counterparty.name,
        'setDate': counterparty.setDate
    }
    return serialized


@app.route('/api/v1/counterparties/<int:counterparty_id>', methods=['PUT'])
@jwt_required()
def api_counterparty_put(counterparty_id):
    item = Counterparty.query.filter(Counterparty.id == counterparty_id).first()
    params = request.json
    if not item:
        return {'message': 'No counterparty with this ID'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    db.session.commit()
    serialized = {
        'id': item.id,
        'sysName': item.sysName,
        'name': item.name,
        'setDate': item.setDate
    }
    return serialized


@app.route('/api/v1/counterparties/<int:counterparty_id>', methods=['DELETE'])
@jwt_required()
def api_counterparty_delete(counterparty_id):
    item = Counterparty.query.filter(Counterparty.id == counterparty_id).first()
    if not item:
        return {'message': 'No counterparty with this ID'}, 400
    db.session.delete(item)
    db.session.commit()
    return '', 204


# @app.teardown_appcontext
# def close_session(exception=None):
#     db.session.remove()
