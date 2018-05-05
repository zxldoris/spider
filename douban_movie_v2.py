# -*- coding: utf-8 -*-
# HTMLParser 向解析器喂数据
# feed 投喂数据
# handle_starttag 处理html的开始标签 args：tag：标签名称 attrs：属性列表
import urllib2
from HTMLParser import HTMLParser
import requests


class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
        self.in_movies = False

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                # print('attr', attr)
                if attr[0] == attrname:
                    # print(attr[1])
                    return attr[1]
            return None

        # print('tag',attrs)
        if tag == 'li' and _attr(attrs, 'data-title') and _attr(
                attrs, 'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr(attrs, 'data-title')
            movie['score'] = _attr(attrs, 'data-score')
            movie['director'] = _attr(attrs, 'data-director')
            movie['actors'] = _attr(attrs, 'data-actors')
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)
            self.in_movies = True
        if self.in_movies and tag == 'img' and _attr(
                attrs, 'class') == "" and _attr(attrs, 'rel') == 'nofollow':
            self.in_movies = False
            src = _attr(attrs, 'src')
            movie = self.movies[len(self.movies) - 1]
            movie['poster-url'] = src
            _download_poster_image(movie)


def _download_poster_image(movie):
    src = movie['poster-url']
    r = requests.get(src)
    fname = src.split('/')[-1]
    with open('./img/' + fname, 'wb') as f:
        f.write(r.content)
        movie['poster-path'] = fname


def nowplaying_movies(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0'
        ') Gecko/20100101 Firefox/59.0'
    }
    req = urllib2.Request(url, headers=headers)
    s = urllib2.urlopen(req)
    parser = MovieParser()
    parser.feed(s.read())
    s.close()
    return parser.movies


if __name__ == '__main__':
    url = 'http://movie.douban.com/nowplaying/xiamen/'
    movies = nowplaying_movies(url)

    import json

    print('%s' % json.dumps(
        movies, sort_keys=True, indent=4, separators=(',', ': ')))
