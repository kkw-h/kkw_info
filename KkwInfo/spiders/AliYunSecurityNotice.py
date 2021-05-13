import scrapy


class AliyunsecuritynoticeSpider(scrapy.Spider):
    name = 'aliyun_security_notice'
    allowed_domains = ['help.aliyun.com']
    start_urls = ['https://help.aliyun.com/noticelist/9213612.html']

    def parse(self, response, **kwargs):
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
                'date': dates[key] + times[key],
                'url': 'https://help.aliyun.com' + urls[key]
            })
            key += 1
        return data