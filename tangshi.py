# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import requests


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


class PoemContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = []
        self.in_div = False
        # self.in_p = False

    def _attr(self, attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self._attr(
                attrs, 'class') == 'contson' and self._attr(attrs, 'id'):
            self.in_div = True
        # if self.in_div and tag == 'p':
        #     self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div = False
        # if tag == 'p':
        #     self.in_p = False

    def handle_data(self, data):
        if self.in_div and not self.in_p:
            self.content.append(data)


def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    # print(r.content)
    parser = TangshiParser()
    parser.feed(r.content)
    return parser.tangshis


def download_poem(poem):
    url = poem['url']
    r = requests.get(url)
    parser = PoemContentParser()
    parser.feed(r.content)
    poem['content'] = '\n'.join(parser.content)


if __name__ == '__main__':
    titles = retrive_tangshi_300()
    print(len(titles))

    for i in range(len(titles)):
        with open('tangshi.txt', 'a+') as f:
            f.write('#%d downloading poem form: %s\n' % (i, titles[i]['url']))
            download_poem(titles[i])
            f.write('标题: %(title)s\t作者：%(writer)s\n%(content)s' % (titles[i]))