import scrapy, datetime, urllib.parse


class ChinafilmSpider(scrapy.Spider):
    name = 'china_film'
    allowed_domains = ['www.chinafilm.org.cn']
    start_urls = ['http://www.chinafilm.org.cn/HyAsp/Hy_Index/AjaxGetDateFunction.asp']

    def start_requests(self):
        data = {
            'Year': str(datetime.datetime.now().year),
            'Month': str(datetime.datetime.now().month),
            'oper': str(1)
        }
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=data, callback=self.parse)

    def parse(self, response, **kwargs):
        Films = []
        if response.body is not None:
            FilmList = eval(response.body)
            if len(FilmList['Table'][0]['Info']):
                for Film in FilmList['Table'][0]['Info']:
                    date_str = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/' + str(
                        datetime.datetime.now().day)
                    if date_str == Film['ShowDate']:
                        title_str = Film['FilmName'].replace('%u', '\\u').encode('utf-8').decode('unicode_escape')
                        title = urllib.parse.unquote(title_str, encoding='Windows-1252')
                        Films.append({
                            'id': title,
                            'title': title,
                            'date': Film['ShowDate']
                        })
        return Films
