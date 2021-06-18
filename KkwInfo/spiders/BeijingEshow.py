import scrapy, datetime


class BeijingEshowSpider(scrapy.Spider):
    name = 'beijing_eshow'
    allowed_domains = ['beijing.eshow365.com']
    start_urls = ['http://beijing.eshow365.com/']

    def parse(self, response, **kwargs):
        titles = response.xpath("//ul[@id='ul1']/li/a[@class='zhtitle']/text()").getall()
        address = response.xpath("//ul[@id='ul1']/li/a[@class='cg']/text()").getall()
        times = response.xpath("//ul[@id='ul1']/li/span[@class='time']/text()").getall()
        num = 0
        last_day = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y/%m/%d")
        eshow_list = []
        for title in titles:
            title = title.lstrip()
            addr = address[num].lstrip()
            time = times[num].lstrip()
            if time == last_day:
                eshow_list.append({
                    'id': title + time,
                    'title': title,
                    'address': addr,
                    'time': time
                })
            num += 1
        return eshow_list