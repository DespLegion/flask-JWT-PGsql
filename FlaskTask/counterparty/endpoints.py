# from .ser_schemas import auth_reqparser
from flask import jsonify
from flask_restx import Namespace, Resource
from .ser_schemas import custom_greeting_parser, counterparty_fields, comp_reqparser
from FlaskTask.models.c_models import Counterparty

counterparty_ns = Namespace(name="counterparty", validate=True)


@counterparty_ns.route('/', methods=['GET'])
# @jwt_required()
class GetCounterparties(Resource):

    # @comp_ns.doc('custom_hello')
    # @counterparty_ns.expect(comp_reqparser)
    # @comp_ns.marshal_with(counterparty_fields)
    # @comp_ns.marshal_list_with(counterparty_fields)
    # @comp_ns.doc(params={'id': 'An ID'})
    # @counterparty_ns.marshal_list_with(counterparty_fields)
    def get(self):
        counterparties = Counterparty.query.all()
        serialized = []
        for counterparty in counterparties:
            serialized.append({
                'name': counterparty.name
            })
        return jsonify(serialized)

