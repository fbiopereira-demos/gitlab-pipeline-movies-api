from flask import Flask
from flask_restplus import Api
from flask_pymongo import PyMongo
from config import config
from .services.monit import HealthApi, InfoApi
from app.services import *
from app.custom_log import CustomLog
from app.helpers import get_service_version
import os
from prometheus_flask_exporter import PrometheusMetrics
from .services.monit import support_namespace
from app.services.v1 import v1_namespace


config_name = os.environ.get('ENVIRONMENT')

log = CustomLog(get_service_version(), service_name=os.environ.get('SERVICE_NAME'))

flask_app = Flask(__name__)
flask_app.config.from_object(config[config_name])
flask_app.config['RESTPLUS_VALIDATE'] = True
flask_app.config['ERROR_404_HELP'] = False


metrics = PrometheusMetrics(flask_app)
mongodb = PyMongo(flask_app)

flask_app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ['get', 'post']

service_api = Api(app=flask_app,  doc="/docs", version=get_service_version(),
          title="Filmes", description="Cadastro de Filmes <style>.models {display: none !important}</style>",
          validate=True, catch_all_404s=False)

service_api.add_namespace(support_namespace.support_namespace, path="/monit")
service_api.add_namespace(v1_namespace.v1_namespace, path="/api/v1")
