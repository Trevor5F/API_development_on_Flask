from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from helpers.decorators import auth_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        r = director_service.get_one(id)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200
