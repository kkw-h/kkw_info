import datetime, requests, os
from loguru import logger
import KkwInfo.spiders


def get_date():
    date = {
        'Year': str(datetime.datetime.now().year),
        'Month': str(datetime.datetime.now().month),
        'Day': str(datetime.datetime.now().day)
    }
    return date


def send_msg(json, name):
    chanify_host = os.getenv('MSG_URL')
    if os.getenv(name.swapcase()):
        chanify_token = os.getenv(name.swapcase())
    else:
        chanify_token = os.getenv('CHANIFY_TOKEN')

    url = chanify_host + chanify_token
    if json is not None:
        requests.post(url=url, json=json)


def get_date_str(utc):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_time = datetime.datetime.strptime(utc, UTC_FORMAT)
    return (utc_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_division_list(lists: list, num: int):
    return [lists[i:i + num] for i in range(0, len(lists), num)]


def show_logs(text: str):
    """
    显示Log
    :param text:
    :return:
    """
    logger.info(text)
