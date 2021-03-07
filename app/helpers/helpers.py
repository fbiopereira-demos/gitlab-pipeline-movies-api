from flask import request
from app.custom_error import BaseError, GeneralUnexpectedError
from hamcrest import assert_that, has_key, has_entry
import app
from threading import Thread
from git import Repo, TagReference
import os
from datetime import datetime


def check_exceptions(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BaseError as ex:
            app.log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                          http_status=ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status
        except Exception as ex:
            ex = GeneralUnexpectedError(app.flask_app.config['SERVICE_NAME'], str(ex))
            app.log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                          http_status=ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status

    return wrapper


def build_response(error_code, message, response, status_code):
    return {
        "error_code": error_code,
        "message": message,
        "response": response
    }, status_code


def build_working_response(service, status, error_description='', error_code=''):
    return {
        "service": service,
        "status": status,
        "error_description": error_description,
        "error_code": error_code
    }


def log_request(f):
    def wrapper(*args, **kwargs):
        message = "Method: " + str(request.method) + " endpoint: " + request.full_path + " body: "
        if request.data:
            message += str(request.data)

        app.log.info(class_name='helpers', method='log_request',
                     http_status=200, message='Request recebido: ' + message)
        response = f(*args, **kwargs)
        return response
    return wrapper


def process_async(async_function):
    def decorator(f):
        def wrapper(*args, **kwargs):
            thread = Thread(target=async_function, args=args, kwargs=kwargs)
            thread.start()
            return f(*args, **kwargs)
        return wrapper
    return decorator


def get_git_repo():
    git_path = os.path.dirname(os.path.abspath(__file__))
    if os.name != 'nt':
        git_path = git_path.replace("/app/helpers", "")
    else:
        git_path = git_path.replace("\\app\\helpers", "")
    repo = Repo(git_path)
    return repo


def get_git_last_commit():
    return str(get_git_repo().head.commit)[0:8]


def get_git_last_tag():
    try:
        repo = get_git_repo()
        tag_ref = repo.tags[len(repo.tags) - 1]
        if tag_ref is not None:
            return str(tag_ref)
        else:
            return 'n0.0.0'
    except Exception:
        return 'e0.0.0'


def get_service_version():
    if app.config_name != 'production':
        return get_git_last_commit()
    else:
        return get_git_last_tag()


def get_server_datetime():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt

