import scrapy, json
from KkwInfo.util.Tool import get_date_str


class EpicfreegamesSpider(scrapy.Spider):
    name = 'epic_free_games'
    allowed_domains = ['store-site-backend-static.ak.epicgames.com']
    start_urls = [
        'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=US&allowCountries=US']

    def parse(self, response, **kwargs):
        data = json.loads(response.body)
        lists = data['data']['Catalog']['searchStore']['elements']
        game_list = []
        for info in lists:
            if info['promotions'] is not None:
                game_list.append({
                    'id': info['title'],
                    'title': info['title'],
                    'start_date': get_date_str(info['effectiveDate'])
                })
        return game_list
