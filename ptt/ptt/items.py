# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PttItem(scrapy.Item):
    title = scrapy.Field()              #標題
    date = scrapy.Field()               #發文時間
    url = scrapy.Field()                #網址
    content = scrapy.Field()            #內文
    store = scrapy.Field()              #店家名稱
    product = scrapy.Field()            #商品名稱
    comments = scrapy.Field()           #評論
