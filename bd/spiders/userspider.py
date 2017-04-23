import scrapy
from pymongo import MongoClient

class userspider(scrapy.Spider):
    start_urls = []
    name = 'userspider'
    baseUrl = "http://www.panduoduo.net/u/bd/"
    global user
    index = 1
    count = 0
    client = MongoClient('127.0.0.1', 27017)
    db_name = 'baidu'
    db = client[db_name]
    user = db['user']
    while(index <= count):
        url = baseUrl + str(index)
        start_urls.append(url)
        index += 1



    def parse(self, response):
        global user
        result = response.xpath("//div[@class='user']")
        for index, link in enumerate(result):
            avatar = link.xpath("//img[@class='avatar']/@src").extract()
            username = link.xpath("//div[@class='info']/a[2]/text()").extract()
            uks = link.xpath("//div[@class='info']/a[1]/@href").extract()
            uk = uks[index][6:]
            obj = {"uk":uk,"username":username[index],"avatar":avatar[index]}
            user.insert(obj)

            print uk
            print avatar[index]
            print username[index]


