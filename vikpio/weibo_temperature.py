# coding=utf-8
from weibo import APIClient
import os
import sys


APP_KEY = 'x'
APP_SECRET = 'x'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'


def get_access_token(app_key, app_secret, callback_url):
    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)
    # 获取授权页面网址
    auth_url = client.get_authorize_url()
    print auth_url

    # 在浏览器中访问这个URL，会跳转到回调地址，回调地址后面跟着code，输入code
    code = raw_input("Input code:")
    r = client.request_access_token(code)
    access_token = r.access_token
    # token过期的UNIX时间
    expires_in = r.expires_in
    print 'access_token:', access_token
    print 'expires_in:', expires_in

    return access_token, expires_in


def init_login(login=False):
    access_token = ""
    expires_in = ""
    app_key = APP_KEY
    app_secret = APP_SECRET
    callback_url = CALLBACK_URL
    if login:
        access_token, expires_in = get_access_token(app_key, app_secret, callback_url)
        # 上面的语句运行一次后，可保存得到的access token，不必每次都申请
        print "access_token = %s, expires_in = %s" % (access_token, expires_in)
        # access_token = 'xxxxxxxx'
        # expires_in = 'xxxxxx'
        with open('./access_token', 'w') as f:
            f.write("%s\n%s\n" % (access_token,expires_in))
        return

    with open('./access_token', 'r') as f:
        str = f.readline()
        access_token = str[:-1]
        str = f.readline()
        expires_in = str[:-1]

    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)
    client.set_access_token(access_token, expires_in)
    return client


def send_mes(client, message):
    utext = unicode(message, "UTF-8")
    client.post.statuses__share(status=utext)
    print u"发送成功！"


if __name__ == '__main__':
    if len(sys.argv) == 2:
        strArr = str(sys.argv)
        if sys.argv[1] != "login":
            print "error"
        init_login(True)
    else:
        temp = ""
        humidity = ""
        pressure = ""
        with open('./temperature.txt', 'r') as f:
            temp = f.readline()
            humidity = f.readline()
            pressure = f.readline()
        msg = "疑似AI的raspberry播报室内环境舒适度:\n温度:%s 湿度:%s 气压:%s" % (temp, humidity, pressure)
        client = init_login()
        mes = msg + "http://victoriest.me"
        send_mes(client, mes)
