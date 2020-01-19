import json
from os.path import join, dirname, isfile
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

movie_fname = join(dirname(__file__), 'movie.json')


def get_movies():
    default_url = 'https://movie.naver.com/movie/'
    r = requests.get(urljoin(default_url, 'sdb/rank/rmovie.nhn?sel=pnt&date=20190909'))
    soup = BeautifulSoup(r.text, 'html.parser')
    movies = soup.select('#old_content > table > tbody > tr')

    movs = []
    i = 1

    for movie in movies:
        movie_name = movie.select_one('.title a')
        if movie_name is not None:
            movie_rating = movie.select_one('.point').text

            movie_info = {'rank': i, 'name': movie_name.text, 'rating': movie_rating,
                          'url': urljoin(default_url, movie.select_one('td.title a')['href'])}
            movs.append(movie_info)
            i += 1

    for movie in movs:
        r = requests.get(urljoin(default_url, movie['url']))
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            movie['image'] = soup.select_one('div.mv_info_area div.poster a > img')['src']
        except (TypeError, KeyError):
            movie['image'] = ''

    if not isfile(movie_fname):
        with open(movie_fname, 'w') as f:
            f.write(json.dumps(movs))

    return movs


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_movies())
