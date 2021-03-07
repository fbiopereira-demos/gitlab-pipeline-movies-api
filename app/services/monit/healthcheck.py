from flask_restplus import Resource
from app.helpers import check_exceptions, log_request
from .support_namespace import support_namespace

@support_namespace.route("/healthcheck")
class HealthApi(Resource):
    @log_request
    @check_exceptions
    def get(self):
        return "It's alive", 200
