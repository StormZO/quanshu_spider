# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
# from scrapy.settings import MongoDBname, MongoItem
MongoDBname = 'quanshu'     #  数据库名
MongoItem = 'novel'         #  数据库集合名

class QuanshuPipeline(object):
    def __init__(self):
        dbName = MongoDBname             # 给数据库添加名字
        client = MongoClient()           # 创建连接对象client
        db = client[dbName]              # 使用的数据库
        self.post = db[MongoItem]

    def process_item(self, item, spider):
        item = dict(item)
        self.post.insert(item)
        return item
