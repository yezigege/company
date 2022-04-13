# -*- coding: utf-8 -*-
import json
import sys

from flask import jsonify, current_app


class RetCodeAndMessage(object):
    Base = 0
    Success = (Base, u"成功")
    Fail = (500, u"服务器内部错误")
    LOCK = (600, u"触发数据库写锁")
    Illegal_Operation = (9999, "非法操作")

    class Common(object):
        CommonBase = 1000
        NOT_SUPPORT_OPERATE = (CommonBase + 1, u'不支持的操作')
        FormatError = (CommonBase + 2, u'请求参数格式错误')
        MISS_PARAMETER = (CommonBase + 3, u'缺少参数')
        INVALID_PARAMS_GROUP = (CommonBase + 4, u'非法参数组合')
        BAD_PARAMETER = (CommonBase + 5, u'参数错误')
        NO_PERMISSION = (CommonBase + 6, u'没有权限')
        SDK_RESPONSE_ERROR = (CommonBase + 7, u'sdk接口返回错误')
        INVALID_OPTIONS = (CommonBase + 8, u'非法操作')
        INVALID_PARAMS = (CommonBase + 9, u'非法参数')

        @staticmethod
        def miss_obj(table_name):
            return RetCodeAndMessage.Common.CommonBase + 100, '%s数据不存在' % table_name

    class Hello(object):
        HelloBase = 2000
        HelloOther = (HelloBase + 1, u'其他错误')


def response(ret_code_and_message=None, data=None, args=None, cache=False, cache_time=10):
    """
    返回值格式化
    :param ret_code_and_message: 校验码
    :param data: 实用数据
    :param args: 接受到的数据
    :param cache: 是否缓存返回值
    :param cache_time: 缓存时长，默认10秒
    :return:
    """
    ret_data = {}
    ret_data["code"] = ret_code_and_message[0]
    ret_data["msg"] = ret_code_and_message[1]

    if data is not None:
        ret_data['data'] = data

    if args is not None:
        ret_data['args'] = args

    # 缓存返回值
    if cache:
        cache_key = sys._getframe(1).f_code.co_name
        current_app.redis.setex(cache_key, cache_time, json.dumps(ret_data))

    return jsonify(ret_data), 200

