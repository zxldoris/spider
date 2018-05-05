# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser


# 登陆豆瓣类
class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'origin': 'http://www.douban.com'
        }
        # 将headers添加到会话中去，整个会话中headers都会有headers里面的字段
        self.session = requests.session()
        self.session.headers.update(headers)

    # 登录
    def login(self,
              username,
              password,
              source='abc',
              redir='https://www.douban.com/',
              login='登录'):
        # 访问登录页面 获取验证码信息
        url = 'https://www.douban.com/accounts/login'
        r = self.session.get(url)
        # 从_get_captcha函数中获取验证码id和url
        (captcha_id, captcha_url) = _get_captcha(r.content)
        # 如果获取到captcha_id 让用户输入验证码
        if captcha_id:
            captcha_solution = raw_input(
                'please input solution for captcha [%s]:' % captcha_url)
        # 构建表单
        data = {
            'form_email': username,
            'form_password': password,
            'source': source,
            'redir': redir,
            'login': login
        }
        headers = {
            'referer': 'http://www.douban.com/accounts/login',
            'host': 'accounts.douban.com'
        }
        # 将captcha-id captcha-solution 添加到表单中
        if captcha_id:
            data['captcha-id'] = captcha_id
            data['captcha-solution'] = captcha_solution

        # https://www.douban.com/login
        # 发送表单
        self.session.post(url, data=data, headers=headers)
        print(self.session.cookies.items())

    def edit_signature(self, username_id, signature):
        # 获取ck
        url = 'https://www.douban.com/people/%s/' % username_id
        r = self.session.get(url)
        # post请求， 修改签名
        data = {'ck': _get_ck(r.content), 'signature': signature}
        url_edit_signature = 'https://www.douban.com/j/people/%s/edit_signature' % username_id
        headers = {
            'referer': url_edit_signature,
            'host': 'www.douban.com'
            # 'x-requested-with': 'XMLHttpRequest'
        }
        r = self.session.post(url_edit_signature, data=data, headers=headers)
        print(r.content)


# 获取需要得到的属性名的值
def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


# 获取验证码url id
def _get_captcha(content):
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None

        def handle_starttag(self, tag, attrs):
            # 获取captcha_id的值
            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(
                    attrs, 'name') == 'captcha-id':
                self.captcha_id = _attr(attrs, 'value')

            # 获取captcha_url的值
            if tag == 'img' and _attr(
                    attrs, 'id') == 'captcha_image' and _attr(
                        attrs, 'alt') == 'captcha' and _attr(
                            attrs, 'class') == 'captcha_image':
                self.captcha_url = _attr(attrs, 'src')

    p = CaptchaParser()
    p.feed(content)
    return p.captcha_id, p.captcha_url


def _get_ck(content):
    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck = None

        def handle_starttag(self, tag, attrs):
            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(
                    attrs, 'name') == 'ck':
                self.ck = _attr(attrs, 'value')

    p = CKParser()
    p.feed(content)
    return p.ck


if __name__ == '__main__':
    c = DoubanClient()
    c.login('1281920478@qq.com', 'zaq1111111111')
    c.edit_signature('178175165', 'test8')
