from flask_apispec import use_kwargs
from marshmallow import fields, validate

from errors import BaseError
from schema import hello_schema
from util.blueprint import RootBlueprint
from util.flask_apispec import marshal_with
from util.response_util import RetCodeAndMessage, response


hello_bp = RootBlueprint('hello', __name__,  url_prefix='/views/hello')


@hello_bp.route('/', methods=['GET'])
@use_kwargs({
    "name": fields.String(required=True, description="姓名"),
    "gender": fields.Integer(required=True, validate=validate.OneOf([-1, 0, 1]), description="性别 0 女 1 男 -1 未知")
    }, location="query")
@marshal_with(hello_schema.HelloSchema)
def hello(name: str, gender: int):
    if name == "raise":
        raise BaseError(RetCodeAndMessage.Hello.HelloOther)
    return {"info": f"name: {name}, gender: {gender}"}
    # return response(RetCodeAndMessage.Success)


@hello_bp.route('/sentry', methods=['GET'])
def sentry():
    """用来测试 sentry 异常记录框架"""
    division_by_zero = 1 / 0
    return {division_by_zero: division_by_zero}