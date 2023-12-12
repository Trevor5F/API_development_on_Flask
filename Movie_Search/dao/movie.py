from flask_restx import abort

from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session


    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self, filters):
        t = self.session.query(Movie)

        if "director_id" in filters:
            t = t.filter(Movie.director_id == filters.get("director_id"))
        if "genre_id" in filters:
            t = t.filter(Movie.genre_id == filters.get("genre_id"))
        if "year" in filters:
            t = t.filter(Movie.year == filters.get("year"))
        if "status" in filters:
            if filters.get("status") == "new":
                t = t.order_by(Movie.year.desc())
        if "page" in filters:
            page_num = int(filters["page"])
            t = t.limit(12).offset((page_num - 1) * 12)
        return t.all()


    def create(self, movie_d):
        ent = Movie(**movie_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_one(rid)
        self.session.delete(movie)
        self.session.commit()

    def update(self, movie_d):
        movie = self.get_one(movie_d.get("id"))

        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self.session.add(movie)
        self.session.commit()

    def partial_update(self, movie_d):
        movie = self.get_one(movie_d.get("id"))
        for key, value in movie_d.items():
            setattr(movie, key, value)
        self.session.commit()
