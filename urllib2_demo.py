import urllib2
import urllib
import cookielib

# urllib2.Request 提供http header 定制功能 能处理cookie
# urllib2.urlopen(timeout=3) 提供超时设置
# urllib.urlencode
# urllib2.build_opener 定制http的行为

# cookielib.CookieJar 提供解析并保存cookie的接口
# HTTPCookieProcessor 提供自动处理cookie的功能


def urlopen():
    url = 'http://blog.kamidox.com/no-exit'
    try:
        s = urllib2.urlopen(url, timeout=3)
    except urllib2.HTTPError, e:
        print(e)
    else:
        print(s.read(100))
        s.close()


def request():
    headers = {"User-Agent": "Mozilla/5.0", 'x-my-header': 'my header'}
    req = urllib2.Request('https://www.douban.com', headers=headers)
    s = urllib2.urlopen(req)
    print(s.read(100))
    print("req.headers:", req.headers)
    s.close()


def request_post_debug():
    # POST
    data = {'username': 'doris', 'password': 'xxxxxxxx'}
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0'
    }
    req = urllib2.Request(
        'http://www.douban.com', data=urllib.urlencode(data), headers=headers)
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    s = opener.open(req)
    print(s.read(100))
    s.close()


def install_debug_handler():
    opener = urllib2.build_opener(
        urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPSHandler(debuglevel=1))
    urllib2.install_opener(opener)


# cookie 处理函数
def handle_cookie():
    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
    opener = urllib2.build_opener(handler, urllib2.HTTPSHandler(debuglevel=1))
    s = opener.open('https://www.douban.com')
    print(s.read(100))
    s.close()

    print('#'*80)
    print(cookiejar._cookies)
    print('#'*80)

    s = opener.open('https://www.douban.com')
    s.close()


if __name__ == '__main__':
    # install_debug_handler()
    # request()
    handle_cookie()
