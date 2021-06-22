import scrapy, datetime, urllib.parse, random, time


class ChinafilmSpider(scrapy.Spider):
    name = 'china_films'
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
                    print(Film['FilmName'].replace('%u', '\\u').encode('utf-8').decode('unicode_escape'))
                    if date_str == Film['ShowDate']:
                        title_str = Film['FilmName'].replace('%u', '\\u').encode('utf-8').decode('unicode_escape')
                        title = urllib.parse.unquote(title_str, encoding='Windows-1252')
                        info = {
                            'id': title + str(Film['fid']),
                            'fid': Film['fid'],
                            'title': title,
                            'date': Film['ShowDate']
                        }
                        time_str = str(time.time()).replace('.', '')[:-3]
                        url = self.start_urls[0] + '?' + str(random.random()) + f'&rad={time_str}'
                        post_data = {
                            'oper': '2',
                            'fid': str(Film['fid'])
                        }
                        yield scrapy.FormRequest(url=url, formdata=post_data, callback=self.parse_content,
                                                 cb_kwargs=dict(info=info))

    def parse_content(self, response, info):
        FilmInfo = eval(response.body)
        FilmInfo = FilmInfo['Table'][0]
        for key in FilmInfo:
            str_str = FilmInfo[key].replace('%u', '\\u').encode('utf-8').decode('unicode_escape')
            FilmInfo[key] = urllib.parse.unquote(str_str, encoding='Windows-1252')
            info[key] = FilmInfo[key]
        return info

