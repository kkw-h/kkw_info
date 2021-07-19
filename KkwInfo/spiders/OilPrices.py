import scrapy
from KkwInfo.util.Tool import get_date
from loguru import logger

class OilpricesSpider(scrapy.Spider):
    name = 'oil_prices'
    allowed_domains = ['www.qiyoujiage.com']
    start_urls = [
        'http://www.qiyoujiage.com/henan.shtml',
        'http://www.qiyoujiage.com/beijing.shtml'
    ]

    def parse(self, response, **kwargs):
        logger.info('油价')
        data = []
        titles = response.selector.xpath("//div[@id='youjia']/dl/dt/text()").getall()
        prices = response.selector.xpath("//div[@id='youjia']/dl/dd/text()").getall()
        key = 0
        date = get_date()
        date_str = date['Year'] + '-' + date['Month'] + '-' + date['Day']
        for title in titles:
            data.append({
                'id': title + date_str,
                'title': title,
                'price': prices[key],
                'date': date_str
            })
            key += 1
        return data
