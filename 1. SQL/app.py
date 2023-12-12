import json

from flask import Flask, jsonify
from utils import search_by_title, movie_year, by_ratings, movie_genre

app = Flask(__name__)

@app.route("/movie/<title>")
def get_title(title):
    return jsonify(search_by_title(title))

@app.route("/movies/<int:start_year>/to/<int:end_year>")
def search_by_period(start_year, end_year):
    return jsonify(movie_year(start_year, end_year))

@app.route("/rating/<group>")
def search_by_rating(group):
    ratings = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    if group in ratings:
        return jsonify(by_ratings(ratings[group]))

@app.route("/genre/<genre>")
def get_genre(genre):
    return jsonify(movie_genre(genre))

app.run()