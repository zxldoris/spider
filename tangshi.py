# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import requests
import re


class TangshiParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tangshis = []
        self.in_div = False
        self.in_a = False
        self.in_span = False
        self.current_poem = {}
        self.writer = False
        self.title = False

    def _attr(self, attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self._attr(attrs, 'class') == 'typecont':
            self.in_div = True
        if self.in_div and tag == 'span':
            self.in_span = True

        if self.in_span and tag == 'a' and self._attr(
                            attrs, 'href') and self._attr(attrs, 'target') == '_blank':
            self.in_a = True
            self.current_poem['url'] = self._attr(attrs, 'href')

    # def handle_endtag(self, tag):
        #     if tag == 'div':
        #         self.in_div = False
        #     if tag == 'span':
        #         self.in_span = False
        #     if tag == 'a':
        #         self.in_a = False
        #
    def handle_data(self, data):
        if data:
            if self.in_span:
                self.current_poem['title'] = data
                self.title = True
            if self.in_a:
                self.current_poem['writer'] = data
                self.writer = True
            if self.writer and self.title:
                # self.in_div = False
                self.in_a = False
                # self.in_span = False
                self.title = False
                self.writer = False
                self.tangshis.append(self.current_poem)
                self.current_poem = {}

def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    # print(r.content)
    parser = TangshiParser()
    parser.feed(r.content)
    return parser.tangshis


if __name__ == '__main__':
    l = retrive_tangshi_300()
    print(len(l))
    for i in range(10):
        print('标题: %(title)s\t作者：%(writer)s\tURL: %(url)s' % (l[i]))
