# -*- coding: UTF-8 -*-

import os
import urllib
import requests
from HTMLParser import HTMLParser
import chardet


class ATTR(object):
    def _attr(self, attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None


class URLParser(HTMLParser, ATTR):
    def __init__(self):
        HTMLParser.__init__(self)
        self.urllist = []
        self.in_li = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li' and self._attr(
                attrs, 'class') == ' j_thread_list clearfix' and self._attr(
                    attrs, 'data-field'):
            self.in_li = True
        if self.in_li and tag == 'a' and self._attr(
                attrs, 'class') == 'j_th_tit ' and self._attr(
                    attrs, 'rel') == 'noreferrer' and self._attr(
                        attrs, 'target') == '_blank':
            print(1)
            self.urllist.append(
                'http://tieba.baidu.com' + self._attr(attrs, 'href'))
            print('http://tieba.baidu.com' + self._attr(attrs, 'href'))

    def handle_endtag(self, tag):
        if tag == 'li':
            self.in_li = False


class ImgNameParser(HTMLParser, ATTR):
    def __init__(self):
        HTMLParser.__init__(self)
        self.userlist = []
        self.in_div_flag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and (
                self._attr(attrs, 'class') ==
                'l_post j_l_post l_post_bright noborder_bottom' or self._attr(
                    attrs, 'class') == 'l_post j_l_post l_post_bright '
                or self._attr(attrs, 'class') ==
                'l_post j_l_post l_post_bright noborder ') and self._attr(
                    attrs, 'data-field'):
            self.in_div_flag = True
        if self.in_div_flag and tag == 'img' and self._attr(
                attrs, 'class') == "" and self._attr(
                    attrs, 'username') and self._attr(attrs, 'src'):
            user = {}
            user['username'] = self._attr(attrs, 'username')
            user['img'] = self._attr(attrs, 'src')
            self.userlist.append(user)
            user = {}


def get_url():
    url = 'http://tieba.baidu.com/f?kw=python&ie=utf-8'
    req = requests.get(url)
    parser = URLParser()
    parser.feed(req.content)
    for url in parser.urllist:
        print(url)
    return parser.urllist


def get_userlist(urllist,file):
    for url in urllist:
        req = requests.get(url)
        parser = ImgNameParser()
        parser.feed(req.content)
        users = parser.userlist
        download_img(users,file)


def download_img(users,file):
    if not os.path.isdir(file):
        os.mkdir(file)
    for user in users:
        fname = file+user['username']+".jpg"
        fname = fname.decode('utf-8')
        fname = fname.encode('GBK')
        urllib.urlretrieve(user['img'], fname)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # urllist = get_url()
    urllist = ['http://tieba.baidu.com/p/5683271835']
    get_userlist(urllist, 'baidu_tieba_img/')
