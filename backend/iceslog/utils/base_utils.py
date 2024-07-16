


from json import JSONEncoder
import json
import logging
import math
import random
from urllib.parse import unquote
from datetime import datetime
import sys

INT_MAX = sys.maxsize

def random_int(num=255):
    return random.randint(0, num)

rand_array = [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
        'x', 'y'
    ]
def random_url(num=5):
    result = ''
    for _ in range(0, num):
        result = result + random.choice(rand_array)
    return result

ranhex_array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

def random_hex(num=32):
    result = ''
    for _ in range(0, num):
        result = result + random.choice(ranhex_array)
    return result



def super_transfer(_type, value, default_return=0, is_log=False):
    try:
        result = _type(value)
    except:
        result = default_return
        if is_log:
            logging.error('将{value}转换为{_type}类型时失败'.format(value=value, _type=_type))

    return result

def safe_str(value, default_return="", is_log=False) -> str:
    '''
    提供安全的类型转换函数,将value转换为int类型
    :param value:需要被转换的数据
    :param default_return: 转换失败时的返回值
    :param is_log:是否记录日志
    :return:
    '''
    if not value:
        return ""
    if type(value) == str:
        return value
    try:
        if type(value) == bytes:
            return bytes.decode(value, "utf-8")
        if type(value) == dict:
            return json.dumps(value, cls=JSONEncoder)
        if type(value) == list:
            return json.dumps(value, cls=JSONEncoder)
        result = str(value)
    except:
        result = default_return
        if is_log:
            logging.error('将{value}转换为{_type}类型时失败'.format(value=value))

    return result

def safe_decode(value, default_return="", is_log=False) -> str:
    '''
    提供安全的类型转换函数,将value转换为int类型
    :param value:需要被转换的数据
    :param default_return: 转换失败时的返回值
    :param is_log:是否记录日志
    :return:
    '''
    if not value:
        return ""
    if type(value) != str:
        value = safe_str(value)
    try:
        result = unquote(value)
    except:
        result = default_return
        if is_log:
            logging.error('将{value}转换为{_type}类型时失败'.format(value=value))

    return result


def safe_int(value, default_return=0, is_log=False):
    '''
    提供安全的类型转换函数,将value转换为int类型
    :param value:需要被转换的数据
    :param default_return: 转换失败时的返回值
    :param is_log:是否记录日志
    :return:
    '''
    exce_value = -9999999876
    ret = super_transfer(int, value, exce_value, is_log)
    if ret != exce_value:
        return ret

    return math.floor(super_transfer(float, value, default_return, is_log))


def safe_float(value, default_return=0, is_log=False):
    '''
    提供安全的类型转换函数,将value转换为float类型
    :param value:需要被转换的数据
    :param default_return: 转换失败时的返回值
    :param is_log:是否记录日志
    :return:
    '''
    return super_transfer(float, value, default_return, is_log)


def safe_json(source, default={}):
    '''若转化失败, 则返回默认值'''
    try:
        if not source:
            return {}
        if isinstance(source, bytes):
            source = safe_str(source)
        if not isinstance(source, str):
            return source
        try:
            value = json.loads(source)
            return value
        except:
            pass
        # value = JSONEncoder().encode(source)
        value = eval(source)
        return value
    except Exception as e:
        return default

def print_exec(logging_type=''):
    logging.warning("------------exception occur----------------")
    import traceback
    info = traceback.format_exc()
    logging.error(info)

    error_logging = logging.getLogger('error')
    error_logging.warning("------------exception occur----------------")
    error_logging.error(info)
    
def split_to_int_list(val: str, split="|") -> list[int]:
    if not val or len(val) == 0:
        return []
    rets = []
    for v in (val or "").split(split):
        rets.append(safe_int(v))
    return rets

def join_list_to_str(arr: list, split="|") -> str:
    arr = [str(v) for v in arr]
    return split.join(arr)

def append_split_to_str(val: str, next: any, split="|") -> str:
    if not val or len(val) == 0:
        return f"{next}"
    else:
        return f"{val}{split}{next}"
    
def now() -> datetime:
    return datetime.now()

def get_now_minute(n:datetime = None) -> int:
    if not n:
        n = now()
    return int(n.timestamp() / 60)

def minute_to_datetime(minute: int) -> datetime:
    stamp = minute * 60
    return datetime.fromtimestamp(stamp)

def calc_step_value(start: int, now: int, step: int) -> int:
    s = now - start
    return int(s / step) * step + start

def fix_step(now: int, step: int) -> int:
    return int(now / step) * step