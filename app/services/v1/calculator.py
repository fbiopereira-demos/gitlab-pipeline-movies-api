from flask_restplus import Resource, fields
from app.helpers import check_exceptions, log_request
from .v1_namespace import v1_namespace
from flask import request


post_model = v1_namespace.model('CalculatorpostModel', {
                    'number_1': fields.Integer(required=True),
                    'number_2': fields.Integer(required=True),
                    'operation': fields.String(required=True)
                })

@v1_namespace.route("/calc")
class Calculator(Resource):
    @log_request
    @check_exceptions
    def get(self):
        return "It's alive", 200

    @log_request
    @check_exceptions
    @v1_namespace.doc(body=post_model)
    #@v1_namespace.expect(post_model, validate=True)
    def post(self):
        try:
            result = request.json['number_1'] + request.json['number_2']
            return "O resultado da {} foi {}".format(request.json['operation'], result), 200

        except Exception as ex:
            return 'Erro', 500
