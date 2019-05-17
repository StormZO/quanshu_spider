# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()           #小说类别
    title = scrapy.Field()          #小说名
    author = scrapy.Field()         #作者
    brief = scrapy.Field()          #简介

    book_href = scrapy.Field()      # 小说章节名称
    href = scrapy.Field()           #小说类别url
    chapter_href = scrapy.Field()   #小说章节链接
    chapter_name = scrapy.Field()   #小说链接

