from flask_restplus import Resource
from flask import Response
from app.helpers import check_exceptions, log_request
from .support_namespace import support_namespace
from prometheus_client import generate_latest


@support_namespace.route("/metrics")
class Metrics(Resource):
    @log_request
    @check_exceptions
    def get(self):
        return Response(generate_latest())
