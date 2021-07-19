import scrapy, datetime
from KkwInfo.util.Tool import get_division_list
from loguru import logger

class SecuritytencentSpider(scrapy.Spider):
    name = 'security_tencent'
    allowed_domains = ['security.tencent.com']
    start_urls = ['https://security.tencent.com/index.php/ti']

    def parse(self, response):
        logger.info('腾讯云安全公告')
        titles = response.xpath("//tbody[@class='ti-table-content']/tr/td/text()")
        content_url = response.xpath("//tbody[@class='ti-table-content']/tr/td/a/@href")
        titles = get_division_list(titles, 5)

        num = 0
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        list = []
        for title in titles:
            if date == title[1]:
                list.append({
                    'id': title+content_url[num],
                    'title': titles,
                    'url': content_url[num]
                })
                num += 1
        return list
