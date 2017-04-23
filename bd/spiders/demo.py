import random
import threading
import urllib2
import json

import time
import cookielib
from pymongo import MongoClient

#百度网盘：同一IP快速访问接口会被认定为爬虫，5分钟后恢复

proxy = [{"http":'14.204.22.180:40938'},{"http":'222.85.39.97:808'},{"http":'175.155.25.53:808'}]

def newRequest(url):
    print url
    index = random.randint(0, len(proxy))
    proxy_handler = urllib2.ProxyHandler(proxy[index])
    print proxy[index]
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    request = urllib2.Request(url)
    request.add_header('Referer', 'http://pan.baidu.com/')
    request.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    request.add_header('Accept-Encoding', 'sdch')
    request.add_header('Accept-Language', ' zh-CN,zh;q=0.8')
    request.add_header('User-Agent',
                       ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    request.add_header('X-Requested-With','XMLHttpRequest')
    try:
        response = urllib2.urlopen(request)
        result = response.read()
        print result
        obj = json.loads(result)
        objs = obj['records']
        ass.insert(objs)
    except Exception as ex:
        newRequest(url)
        print str(ex)
        pass

def newUrls():
    while True:
        re = user.find_one({"isSpider": "0"})
        baseUrl = "http://pan.baidu.com/pcloud/feed/getsharelist?category=0&auth_type=1&request_location=share_home&start=0&limit=60&channel=chunlei&clienttype=0&web=1&query_uk="
        url = baseUrl + re['uk']
        re['isSpider'] = "1"
        user.save(re)
        newRequest(url)

client = MongoClient('127.0.0.1', 27017)
db_name = 'baidu'
db = client[db_name]
global user
user = db['user']
global ass
ass = db['ass']
newUrls()







