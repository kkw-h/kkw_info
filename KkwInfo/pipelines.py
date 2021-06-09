# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from KkwInfo.util.Tool import send_msg
from KkwInfo.util.Es import duplicates, save


# 过滤数据
class DuplicatesPipeline:
    def process_item(self, item, spider):
        if item:
            if not duplicates(spider.name, item['id']):
                return item


# 保存数据
class SavePipeline:
    def process_item(self, item, spider):
        if item is not None:
            save(spider.name, item['id'], item)
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
            if spider.name == 'games':
                game_company = ['腾讯', '网易', '米哈游', '哔哩哔哩', '雷霆', '凉屋']
                for game in game_company:
                    if game in item['publishing_unit'] or game in item['operation_unit']:
                        json = {
                            'text': f'{item["title"]} \n 类型:{item["declaration_category"]}\n 出版｜运营{item["publishing_unit"]}｜{item["operation_unit"]}\n 时间{item["date"]}'
                        }
            if json is not None:
                send_msg(json)
