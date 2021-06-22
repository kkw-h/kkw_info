import datetime, requests, os


def get_date():
    date = {
        'Year': str(datetime.datetime.now().year),
        'Month': str(datetime.datetime.now().month),
        'Day': str(datetime.datetime.now().day)
    }
    return date


def send_msg(json):
    chanify_host = os.getenv('MSG_URL')
    chanify_token = os.getenv('CHANIFY_TOKEN')
    url = chanify_host + chanify_token
    if json is not None:
        requests.post(url=url, json=json)


def get_date_str(utc):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_time = datetime.datetime.strptime(utc, UTC_FORMAT)
    return (utc_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
