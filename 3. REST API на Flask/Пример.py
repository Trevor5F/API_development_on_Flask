from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    year = fields.Int()

class AuthorSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()


book_schema = BookSchema()
books_schema = BookSchema(many=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

api = Api(app)
book_ns = api.namespace('books')
authors_ns = api.namespace('authors')

b1 = Book(id=1, name='Harry Potter', year=2000,)
b2 = Book(id=2, name='Le Comte de Monte-Cristo', year=1844)

a1 = Author(id=1, first_name='Joan', last_name='Rowling')
a2 = Author(id=2, first_name='Alexander', last_name='Dumas')



with app.app_context():
    db.create_all()
    with db.session.begin():
        db.session.add_all([b1, b2])
        db.session.add_all([a1, a2])


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        req_json = request.json
        new_book = Book(**req_json)
        with db.session.begin():
            db.session.add(new_book)
        return '', 201


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid: int):  # Получение данных
        try:
            book = db.session.query(Book).filter(Book.id == bid).one()
            return book_schema.dump(book), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid):  # Замена данных
        book = db.session.query(Book).get(bid)
        req_json = request.json

        book.name = req_json.get('name')
        book.year = req_json.get('year')

        db.session.add(book)
        db.session.commit()

        return '', 204

    def patch(self, bid):  # частичное обновление данных
        book = db.session.query(Book).get(bid)
        req_json = request.json

        if 'name' in req_json:
            book.name = req_json.get('name')
        if 'year' in req_json:
            book.year = req_json.get('year')

        db.session.add(book)
        db.session.commit()

        return '', 204

    def delete(self, bid: int):
        book = db.session.query(Book).get(bid)

        db.session.delete(book)
        db.session.commit()

        return '', 204

#________________________________________________________


@authors_ns.route('/')
class AuthorsView(Resource):
    def get(self):
        all_authors = db.session.query(Author).all()
        return authors_schema.dump(all_authors), 200

    def post(self):
        req_json = request.json
        new_author = Author(**req_json)
        with db.session.begin():
            db.session.add(new_author)
        return '', 201


@authors_ns.route('/<int:bid>')
class AuthorView(Resource):
    def get(self, bid: int):  # Получение данных
        try:
            author = db.session.query(Author).filter(Author.id == bid).one()
            return author_schema.dump(author), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid):  # Замена данных
        author = db.session.query(Author).get(bid)
        req_json = request.json

        author.first_name = req_json.get('first_name')
        author.last_name = req_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204

    def patch(self, bid):  # частичное обновление данных
        author = db.session.query(Author).get(bid)
        req_json = request.json

        if 'name' in req_json:
            author.name = req_json.get('first_name')
        if 'year' in req_json:
            author.year = req_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204

    def delete(self, bid: int):
        author = db.session.query(Author).get(bid)

        db.session.delete(author)
        db.session.commit()

        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
