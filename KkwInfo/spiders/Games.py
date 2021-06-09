import scrapy
from KkwInfo.util.Es import duplicates, save


class GamesSpider(scrapy.Spider):
    name = 'games'
    allowed_domains = ['www.nppa.gov.cn']
    start_urls = ['http://www.nppa.gov.cn/nppa/channels/%d.shtml']
    codes = [320]
    host = 'http://www.nppa.gov.cn'
    headers = {
        'Cookie': '__jsluid_h=9cb78f35cd6d4bc398c764e5575daf67',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    def start_requests(self):
        for code in self.codes:
            url = self.start_urls[0] % (code)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, cb_kwargs=dict(code=code))

    def parse(self, response, code):
        page_list = response.css('div.ellipsis a::attr(href)').getall()
        title_list = response.css('div.ellipsis a::text').getall()
        num = 0
        for path in page_list:
            # path = '/nppa/contents/320/76057.shtml'
            es_name = self.name + '_path'
            if not duplicates(es_name, path):
                print(path)
                print(title_list[num])
                num += 1
                url = self.host + path
                save(es_name, path, {'title': title_list[num], 'path': path})
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_content, cb_kwargs=dict(code=code))
            else:
                print('已查询,跳过')

    def parse_content(self, response, code):
        # 标题
        titles = response.xpath("//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[2]/text()").getall()
        # 申报类别
        declaration_category = response.xpath(
            "//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[3]/text()").getall()
        # 出版单位
        publishing_unit = response.xpath(
            "//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[4]/text()").getall()
        # 运营单位
        operation_unit = response.xpath(
            "//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[5]/text()").getall()
        # 文号
        document_number = response.xpath(
            "//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[6]/text()").getall()
        # 出版物号
        publication_number = response.xpath(
            "//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[7]/text()").getall()
        # 时间
        date = response.xpath("//table[@class='trStyle tableOrder']/tbody/tr[@class='item']/td[8]/text()").getall()

        num = 0
        game_list = []
        for title in titles:
            game_list.append({
                'id': str(code) + title,
                'title': title,
                'declaration_category': declaration_category[num],
                'publishing_unit': publishing_unit[num],
                'operation_unit': operation_unit[num],
                'document_number': document_number[num],
                'publication_number': publication_number[num],
                'date': date[num],
            })
            num += 1
        return game_list
