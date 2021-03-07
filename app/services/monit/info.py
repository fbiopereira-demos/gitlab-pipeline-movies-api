from flask_restplus import fields
from flask_restplus import Resource
from app.helpers import get_service_version, get_server_datetime
import app
from .support_namespace import support_namespace


output_model = support_namespace.model('Info', {
    'version': fields.String,
    'environment': fields.String,
    'server_datetime': fields.String,
    'environment_variables': fields.String
})


@support_namespace.route("/info")
@support_namespace.response(200, 'Informações da API')
class InfoApi(Resource):

    @support_namespace.marshal_with(output_model, as_list=True, code=200)
    def get(self):

        info_return = {
            "version": get_service_version(),
            "environment": app.flask_app.config['ENVIRONMENT'],
            "server_datetime": get_server_datetime(),
            "environment_variables": [
                    {"LOG_PATH": app.flask_app.config['LOG_PATH']},
                    {"SERVICE_NAME": app.flask_app.config['SERVICE_NAME']}
                ]
            }

        return info_return, 200



