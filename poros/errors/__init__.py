class BaseError(Exception):
    """不报警，只返回客户端错误信息"""
    code = 20000

    def __init__(self, message=None, data=None):
        self.data = data
        if isinstance(message, str):
            self.code = self.code
            self.message = message
        elif isinstance(message, (tuple, list)):
            self.code = message[0]
            self.message = message[1]
        elif isinstance(message, dict):
            self.code = message.get('code', 0)
            self.message = message.get('msg', "成功")
            self.data = data or message.get('data', {})