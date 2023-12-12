from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError

from dao.model.movie import MovieSchema
from helpers.decorators import check_movie_exists, auth_required, admin_required
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        filters = {}

        if "director_id" in request.args:
            filters["director_id"] = request.args["director_id"]
        if "genre_id" in request.args:
            filters["genre_id"] = request.args["genre_id"]
        if "year" in request.args:
            filters["year"] = request.args["year"]
        if "page" in request.args:
            filters["page"] = request.args["page"]
        if "status" in request.args:
            filters["status"] = request.args["status"]

        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

        # director = request.args.get("director_id")
        # genre = request.args.get("genre_id")
        # year = request.args.get("year")
        # filters = {
        #     "director_id": director,
        #     "genre_id": genre,
        #     "year": year,
        # }


    def post(self):
        try:
            movie = movie_service.create(request.json)
            return "", 201, {"location": f"/movies/{movie.id}"}
        except IntegrityError:
            movie_title = request.json.get('title')
            return f'{movie_title} такое поле уже есть'


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @check_movie_exists
    def get(self, mid):
        movie = movie_service.get_one(mid)
        sm_d = MovieSchema().dump(movie)
        return sm_d, 200

    @check_movie_exists
    def put(self, mid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = mid
        movie_service.update(req_json)
        return "", 204

    @check_movie_exists
    def patch(self, mid):
        req_json = request.json
        req_json["id"] = mid
        movie_service.partial_update(req_json)
        return "", 204

    @auth_required
    @check_movie_exists
    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
