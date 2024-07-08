


from json import JSONEncoder
import json
import logging
import math
from urllib.parse import unquote


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

def print_exec(logging_type=''):
    logging.warning("------------exception occur----------------")
    import traceback
    info = traceback.format_exc()
    logging.error(info)

    error_logging = logging.getLogger('error')
    error_logging.warning("------------exception occur----------------")
    error_logging.error(info)
    
def split_to_int_list(val: str, split=",") -> list[int]:
    rets = []
    for v in val.split(split):
        rets.append(safe_int(v))
    return rets