from flask_restplus import Resource, fields
from app.helpers import check_exceptions, log_request, JSONEncoder
from app.custom_error import GeneralUnexpectedError
from .v1_namespace import v1_namespace
from flask import request
import json
import app


movie_model = v1_namespace.model('Movie Model', {
                    'title': fields.String(required=True, description="Movie Title"),
                    'genre': fields.String(required=True, description="Movie Main Genre"),
                    'director': fields.String(required=True, description="Movie Director Name"),
                    'story': fields.String(required=True, description="Movie Story Writer"),
                    'release_year': fields.Integer(required=True, description="Movie First Release Year")
                })


@v1_namespace.route("/movies")
class MovieApi(Resource):
    @log_request
    @check_exceptions
    def get(self):
        return self.list_all_movies()

    @log_request
    @check_exceptions
    @v1_namespace.doc(body=movie_model, params=movie_model)
    def post(self):
        json_body = request.json
        return self.save_new_movie(json_body)

    def save_new_movie(self, movie_json):
        try:
            app.log.info(200, message="Starting saving new movie in database with json {}".format(str(movie_json)))

            movies_db = app.mongodb.db.movies
            movies_db.insert_one(movie_json)

            app.log.info(
                201,
                message="Saved new movie in database with document {}".format(JSONEncoder().encode(movie_json)))
            return json.loads(str(JSONEncoder().encode(movie_json))), 201
        except Exception as ex:
            raise GeneralUnexpectedError(service_name=app.flask_app.config['SERVICE_NAME'], message="Error saving Movie. EX: {}".format(str(ex)))

    def list_all_movies(self):
        try:
            app.log.info(200, message="Recovering all movies in database")

            movies_db = app.mongodb.db.movies
            movies_cursor = movies_db.find({})
            movie_list = []
            for movie in movies_cursor:
                movie_list.append(movie)

            return json.loads(str(JSONEncoder().encode(movie_list))), 200

        except Exception as ex:
            raise GeneralUnexpectedError(service_name=app.flask_app.config['SERVICE_NAME'],
                                         message="Error retrieving movies. EX: {}".format(str(ex)))