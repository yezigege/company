from marshmallow import fields, schema, EXCLUDE


# 重新定义错误消息提示
fields.Field.default_error_messages = {
    "required": "缺少必要数据",
    "null": "数据不能为空",
    "validator_failed": "非法数据",
    "unknown": None
}


# 传入未知字段时，设定为直接扔掉未知字段。（其他的有 INCLUDE 接受未知字段、RAISE 抛出异常）
class MineMeta(schema.Schema.Meta):
    unknown = EXCLUDE


schema.Schema.Meta = MineMeta