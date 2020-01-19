import json
from os.path import isfile, join, dirname

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.crawl.crawl_movie import get_movies, movie_fname

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

movies = []


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'hello, world!'


@app.route('/api/movies', methods=['GET'])
def movie():
    global movies
    query = request.args.get('query')
    try:
        if not movies:
            if isfile(movie_fname):
                with open(movie_fname, 'r') as f:
                    movies = json.loads(f.read())
            else:
                movies = get_movies()
        ret = []
        if query:
            for movie in movies:
                if movie['name'].find(query) > -1:
                    ret.append(movie)
        else:
            ret = movies
        return jsonify({'result': 'success', 'datas': ret})
    except Exception as e:
        return jsonify({'result': 'failure', 'message': str(e)})
