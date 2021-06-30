import json, re, time


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def getContent(code_str):
    lottery_str = code_str.split('|')
    red = lottery_str[0].split(',')
    blue = lottery_str[1]
    return {'blue': blue, 'red': red}


def is_level(blue, red):
    level = 0
    if blue == 1:
        level = 6
        if red == 6:
            level = 1
        if red == 5:
            level = 3
        if red == 4:
            level = 4
        if red == 3:
            level = 5
    else:
        if red == 6:
            level = 2
        if red == 5:
            level = 4
        if red == 4:
            level = 5
    return level


def contrast(lottery_codes):
    # 对比蓝色球
    me_blue = '11'
    me_red = ['03', '09', '12', '15', '22', '31']
    is_blue = 0
    is_red = 0
    if me_blue == str(lottery_codes['blue']):
        is_blue = 1
    for lottery_code in lottery_codes['red']:
        if me_red.count(str(lottery_code)):
            is_red += 1
    return is_level(is_blue, is_red)


def is_send():
    tm_wday = time.strftime("%w", time.localtime())
    if tm_wday in ['2', '4', '7']:
        return True
    return False
