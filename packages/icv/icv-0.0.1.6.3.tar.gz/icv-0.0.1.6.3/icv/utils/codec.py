# -*- coding: UTF-8 -*-
import demjson

def json_encode(obj, encoding="utf-8"):
    """
    encode obj to json string, like json.dumps()
    :param obj:
    :param encoding:
    :return:
    """
    return demjson.encode(obj, encoding=encoding)


def json_decode(str, encoding="utf-8"):
    """
    decode json string to json object, like json.loads()
    :param str:
    :param encoding:
    :return:
    """
    return demjson.decode(str, encoding=encoding)
