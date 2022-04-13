
import logging
import json
import time

from flask import request
from util.date_util import DateUtil


class LoggerJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.decode('utf8').replace("'", '"')
        elif isinstance(o, Exception):
            return str(o)
        return json.JSONEncoder.default(self, o)


class LoggerBase:
    """封装logging"""

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    @classmethod
    def _get_base_dict(cls, content, *args, **params):
        r_params = request.all_param if request and hasattr(request, 'all_param') else {}
        user_id = request.user.user_id if request and hasattr(request, 'user') else None
        base_dict = {k: v for k, v in dict(
            user_id=user_id, device_id=r_params.get('device_id', None), token=r_params.get('token', None),
            version_name=r_params.get('version_name', None),
            timestamp=int(time.time()*1000), args=args).items() if v}
        base_dict.update(params)
        # if args:
        #     try:
        #         content = content % args
        #     except Exception:
        #         pass
        base_dict.update(content=content)
        base_dict.update(system_time=DateUtil.datetime_to_str(fmt=DateUtil.MS_DATETIME_FORMAT))
        return base_dict

    def info(self, content, *args, exc_info=None, extra=None, stack_info=False, **params):
        base_dict = self._get_base_dict(content, *args, **params)
        self.logger.info(
            json.dumps(base_dict, cls=LoggerJsonEncoder, separators=(',', ':'), ensure_ascii=False),
            *args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    def debug(self, content, *args, exc_info=None, extra=None, stack_info=False, **params):
        base_dict = self._get_base_dict(content, *args, **params)
        self.logger.debug(
            json.dumps(base_dict, cls=LoggerJsonEncoder, separators=(',', ':'), ensure_ascii=False),
            *args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    def warning(self, content, *args, exc_info=None, extra=None, stack_info=False, **params):
        base_dict = self._get_base_dict(content, *args, **params)
        self.logger.warning(
            json.dumps(base_dict, cls=LoggerJsonEncoder, separators=(',', ':'), ensure_ascii=False),
            *args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    def warn(self, content, *args, exc_info=None, extra=None, stack_info=False, **params):
        self.warning(
            content, *args, exc_info=exc_info, extra=extra, stack_info=stack_info, **params)

    def error(self, content, *args, exc_info=None, extra=None, stack_info=False, **params):
        base_dict = self._get_base_dict(content, *args, **params)
        self.logger.error(
            json.dumps(base_dict, cls=LoggerJsonEncoder, separators=(',', ':'), ensure_ascii=False),
            *args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    def __getattr__(self, item):
        ret = None
        if hasattr(self.logger, item):
            ret = getattr(self.logger, item)
        return ret
