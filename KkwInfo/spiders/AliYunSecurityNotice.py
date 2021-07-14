import scrapy
from loguru import logger


class AliyunsecuritynoticeSpider(scrapy.Spider):
    name = 'aliyun_security_notice'
    allowed_domains = ['help.aliyun.com']
    start_urls = ['https://help.aliyun.com/noticelist/9213612.html']

    def parse(self, response, **kwargs):
        logger.info('获取阿里云安全公告')
        titles = response.selector.xpath('//ul/li[@class="y-clear"]/a/text()').getall()
        dates = response.selector.xpath('//ul/li[@class="y-clear"]/span/text()').getall()
        times = response.selector.xpath('//ul/li[@class="y-clear"]/span/span/text()').getall()
        urls = response.selector.xpath('//ul/li[@class="y-clear"]/a/@href').getall()

        data = []
        key = 0
        for title in titles:
            data.append({
                'id': title,
                'title': title,
                'date': f"{dates[key]} {times[key]}",
                'url': 'https://help.aliyun.com' + urls[key]
            })
            logger.info(title)
            key += 1
        return data