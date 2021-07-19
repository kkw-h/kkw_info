import scrapy
from KkwInfo.util.LotteryTool import loads_jsonp, getContent, contrast, is_send
from loguru import logger


class LotterySpider(scrapy.Spider):
    name = 'lottery'
    allowed_domains = ['kaijiang.aicai.com']
    start_urls = ['https://kaijiang.aicai.com/open/sinaGameResult.do?game=101']

    def parse(self, response, **kwargs):
        logger.info('彩票数据')
        data = {}
        if is_send():
            content = loads_jsonp(response.body.decode('utf-8'))
            lottery_codes = getContent(content['result'])
            content_str = content['update'] + '\n'
            content_str += '红色球' + '\n'

            for lottery_code in lottery_codes['red']:
                content_str += lottery_code + " "
            content_str += '\n'
            content_str += '蓝色球' + '\n'
            content_str += lottery_codes['blue'] + '\n'
            print(content_str)
            level = contrast(lottery_codes)
            if level == 0:
                content_str += '未中奖'
            else:
                content_str += str(level) + '等奖'
            data = {
                'id': content['update'],
                'title': content['update'],
                'date': content['update'],
                'content_str': content_str
            }
        return data