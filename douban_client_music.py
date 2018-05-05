# -*- coding: utf-8 -*-
# 获取歌曲名称 歌手名字 豆瓣评分 解析单曲封面图片url 并把图片下载下来

import urllib2
from HTMLParser import HTMLParser
import re


class DoubanMusic(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.musics = []
        self.new_albums_flag = False

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag == 'div' and _attr(attrs, 'class') == 'album-item' and _attr(attrs, 'data-reactid'):
            self.new_albums_flag = True
        # 获取图片
        # and tag == 'img' and _attr(attrs, 'data-reactid') and _attr(attrs, 'width') and _attr(attrs, 'src')
        if self.new_albums_flag and tag == 'img' and _attr(attrs, 'data-reactid'):
            # self.new_albums_flag =False
            music = {}
            music['img-url'] = _attr(attrs, 'src')
            self.musics.append(music)
            print('%(img-url)s' % music)
            self.new_albums_flag = True

        # if self.new_albums_flag == True and tag == 'a' and _attr(attrs,'class') == 'album-title' and _attr(attrs,'target') == '_blank':
        #     music = self.musics[len(self.musics) - 1]
        #     music['music-name'] = tag.content

    # def handle_data(self,data):
    #     return data
def new_music(url):
    html = '<div class="album-item" data-reactid=".0.1.0.$30152732">' \
           '<div class="inner" data-reactid=".0.1.0.$30152732.0">' \
           '<a href="https://music.douban.com/subject/30152732/" target="_blank" data-reactid=".0.1.0.$30152732.0.0">' \
           '<div class="cover" data-reactid=".0.1.0.$30152732.0.0.0">' \
           '<img src="https://img1.doubanio.com/view/subject/m/public/s29699949.jpg" data-reactid=".0.1.0.$30152732.0.0.0.0" width="100%">' \
           '</div>' \
           '</a>' \
           '<a class="album-title" href="https://music.douban.com/subject/30152732/" target="_blank" ' \
           'data-reactid=".0.1.0.$30152732.0.1">' \
           'Dirty Computer' \
           '</a>' \
           '<p data-reactid=".0.1.0.$30152732.0.2">Janelle Monáe</p>' \
           '<div class="star clearfix" data-reactid=".0.1.0.$30152732.0.3">' \
           '<span class="allstar35" data-reactid=".0.1.0.$30152732.0.3.0">' \
           '</span>' \
           '<span class="score" data-reactid=".0.1.0.$30152732.0.3.1">7.6</span>' \
           '</div></div></div>'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0'
            ') Gecko/20100101 Firefox/59.0'
    }
    req = urllib2.Request(url, headers=headers)
    s = urllib2.urlopen(req)
    parser = DoubanMusic()
    print(s.read())
    parser.feed(s.read())
    s.close()
    return parser.musics


if __name__ == '__main__':
    url = 'https://music.douban.com/'
    musics = new_music(url)
    import json

    print('%s' % json.dumps(
        musics, sort_keys=True, indent=4, separators=(',', ': ')))
