# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from KkwInfo.util.Tool import send_msg, show_logs
from KkwInfo.util.Es import duplicates, save
from loguru import logger


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
        logger.info(item)
        if item is not None:
            json = None
            if spider.name in ['apple_support']:
                json = {
                    'link': item['url']
                }
            if spider.name == 'china_films':
                json = {
                    'title': item['title'],
                    'text': f' 时间: {item["date"]} \n\n 主演:{item["KS_Starring"]} \n\n 导演:{item["KS_Director"]}'
                            f' \n\n 编剧:{item["KS_Writers"]} \n\n 发行：{item["KS_TheIssuer"]} \n\n'
                            f' 出品:{item["KS_Producers"]} \n\n 类型:{item["KS_Type"]} \n\n 简介:{item["ArticleContent"]}'
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
                            'title': {item["title"]},
                            'text': f'出版｜运营{item["publishing_unit"]}｜{item["operation_unit"]}\n 时间{item["date"]}'
                        }
            if spider.name == 'beijing_eshow':
                json = {
                    'title': item['title'],
                    'text': f'地址:{item["address"]} \n 时间:{item["time"]}'
                }
            if spider.name == 'epic_free_games':
                json = {
                    'title': 'Epic免费游戏领取',
                    'text': f'游戏:{item["title"]} \n开始时间:{item["start_date"]}'
                }
            if spider.name == 'security_tencent':
                json = {
                    'title': item['title'],
                    'text': f'链接:{item["url"]}'
                }
            if spider.name == 'weibo':
                if 8000000 < item['heat']:
                    json = {
                        'title': item['title'],
                        'text': f"热度:{item['heat']} \n时间:{item['date']}"
                    }

            if json is not None:
                send_msg(json, spider.name)
