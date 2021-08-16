import scrapy, datetime
from pprint import pprint


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot']

    def parse(self, response):
        ids = response.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-01 ranktop']/text()").getall()
        contents = response.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-02']/a/text()").getall()
        heats = response.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-02']/span/text()").getall()
        num = 0
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        lists = []
        for id in ids:
            try:
                int(id)
                lists.append({
                    'id': f'{date}|{id}',
                    'title': contents[num + 1],
                    'heat': int(heats[num]),
                    'date': date
                })
                num += 1
            except ValueError:
                pass
        return lists