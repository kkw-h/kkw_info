import scrapy


class AppleSupportSpider(scrapy.Spider):
    name = 'apple_support'
    allowed_domains = ['support.apple.com']
    start_urls = ['https://support.apple.com/zh-cn/service-programs']

    def parse(self, response, **kwargs):
        titles = response.selector.xpath('//div[@class="table-responsive"]/p/a/span[@class="icon icon-chevronright"]/text()').getall()
        dates = response.selector.xpath('//div[@class="table-responsive"]/p/span[@class="note"]/text()').getall()
        urls = response.selector.xpath('//div[@class="table-responsive"]/p/a/@href').getall()
        key = 0
        data = []
        for title in titles:
            data.append({
                'id': title,
                'title': title,
                'date': dates[key],
                'url': 'https://' + self.allowed_domains[0] + urls[key],
            })
            key += 1
        return data
