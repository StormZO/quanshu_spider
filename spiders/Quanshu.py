# -*- coding: utf-8 -*-
import scrapy
from ..items import QuanshuItem
from scrapy import Request
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider

class QuanshuSpider(RedisSpider):
    name = 'Quanshu'
    allowed_domains = ['quanshuwang.com']
    #start_urls = ['http://www.quanshuwang.com/']
    redis_key = 'quanshu:start'

    def parse(self, response):      # 获取首页小说的分类
        li_list = response.xpath("//ul[@class='channel-nav-list']/li")
        for li in li_list:
            items = {}
            href = li.xpath("./a/@href").extract_first()                # 小说分类链接
            items['name'] = li.xpath("./a/text()").extract_first()      # 小说类名
            yield Request(
                url=href,
                meta={'items': deepcopy(items)},
                callback=self.parse_detail
            )

    def parse_detail(self, response):    # 主要获取小说的name,author，和next_url
        items = response.meta['items']
        li_list = response.xpath("//ul[contains(@class,'seeWell')]/li")
        for li in li_list:              # 循环获取每一本小说的信息
            book_href = li.xpath("./a/@href").extract_first()      #小说链接
            items['author'] = li.xpath("./span/a[2]/text()").extract_first() #小说标题 名字
            items['title'] = li.xpath("./span/a/@title").extract_first()   #作者
            print('正在获取', items['name'],items['title'],'请稍后……')
            yield Request(
                url=book_href,
                meta={'items': deepcopy(items)},
                callback=self.parse_detail_next
            )
        # 下一页
        next_url = response.xpath("//a[@class='next']/@href").extract_first()
        if len(next_url) > 0:
            yield Request(
                url=next_url,
                meta={'items': response.meta['items']},
                callback=self.parse_detail,
            )

    def parse_detail_next(self, response):
        items = response.meta['items']
        brief = response.xpath("//div[@class='b-info']/div/div/text()").extract()   #简介
        items['brief'] = brief
        chapters = response.xpath("//div[@class='b-oper']/a/@href").extract_first()
        yield Request(
            url=chapters,
            meta={'items': deepcopy(items)},
            callback=self.chapter
        )

    def chapter(self, response):
        items = response.meta['items']
        item = QuanshuItem()
        item['name'] = items['name']
        item['title'] = items['title']
        item['author'] = items['author']
        item['brief'] = items['brief']
        item['chapter_href'] = response.url
        print('正在保存{}数据……'.format(item['title']))
        # item['chapter_href'] = response.xpath("//div[@class='chapterNum']/ul//div[contains(@class,'clearfix')]/li/a/@href").extract()
        # item['chapter_name'] = response.xpath("//div[@class='chapterNum']/ul//div[contains(@class,'clearfix')]/li/a/text()").extract()
        yield item



