# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch7 import Elasticsearch, exceptions
import hashlib, os
from KkwInfo.util.Tool import send_msg

es = Elasticsearch(hosts=os.getenv("ES_HOST"))

# 过滤数据
class DuplicatesPipeline:
    def process_item(self, item, spider):
        if item:
            id = hashlib.md5(item['id'].encode(encoding='UTF-8')).hexdigest()
            try:
                es.get(id=id, index=spider.name)
            except exceptions.NotFoundError:
                return item


# 保存数据
class SavePipeline:
    def process_item(self, item, spider):
        if item is not None:
            id = hashlib.md5(item['id'].encode(encoding='UTF-8')).hexdigest()
            es.index(index=spider.name, body=item, id=id)
            return item


# 发送消息
class SendPipeline:
    def process_item(self, item, spider):
        if item is not None:
            json = None
            if spider.name in ['apple_support']:
                json = {
                    'link': item['url']
                }
            if spider.name == 'china_films':
                json = {
                    'text': item['date'] + '上映电影\n' + item['title']
                }
            if spider.name == 'lottery':
                json = {
                    "text": item['content_str']
                }
            if spider.name == 'oil_prices':
                if '92' in item['title']:
                    json = {
                        "text": item['title'] + item['price'],
                        "title": item['date']
                    }
            if spider.name == 'aliyun_security_notice':
                json = {
                    'text': item['url'] + '\n 时间:' + item['date'] + '\n' + item['title']
                }

            if json is not None:
                send_msg(json)