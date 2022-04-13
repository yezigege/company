import types
import flask
from apispec import yaml_utils
from apispec_webframeworks.flask import FlaskPlugin as FlaskPluginBase
from flask.views import MethodView
from flask_apispec import FlaskApiSpec as FlaskApiSpecBase
from flask_apispec import ResourceMeta
from flask_apispec.annotations import annotate, activate
from flask_apispec.wrapper import Wrapper, unpack, packed
from werkzeug import wrappers

from util import base_util, response_util


class FlaskPlugin(FlaskPluginBase):
    def path_helper(self, operations, *, view, app=None, **kwargs):
        """Path helper that allows passing a Flask view function."""
        rule = self._rule_for_view(view, app=app)
        _operations = yaml_utils.load_operations_from_docstring(view.__doc__)
        if not _operations and rule.methods:
            _tag = base_util.lreplace('/service', '', rule.rule)
            tag = base_util.lreplace('/views', '', _tag).split('/')[1]
            _operations = {method.lower(): {'summary': view.__doc__ or "", 'tags': [tag]}
                           for method in rule.methods if method not in ['OPTIONS', 'HEAD']}
        base_util.dict_merge(operations, _operations)
        if hasattr(view, "view_class") and issubclass(view.view_class, MethodView):
            for method in view.methods:
                if method in rule.methods:
                    method_name = method.lower()
                    method = getattr(view.view_class, method_name)
                    operations[method_name] = yaml_utils.load_yaml_from_docstring(
                        method.__doc__
                    )
        return self.flaskpath2openapi(rule.rule)


class FlaskApiSpec(FlaskApiSpecBase):

    def register_existing_resources(self):
        for name, rule in self.app.view_functions.items():
            try:
                # fix 蓝图名称包含'.'
                blueprint_name = name[::-1].split('.', 1)[-1][::-1]
            except ValueError:
                blueprint_name = None

            try:
                self.register(rule, blueprint=blueprint_name)
            except TypeError:
                pass

    def _register(self, target, endpoint=None, blueprint=None,
                  resource_class_args=None, resource_class_kwargs=None):
        """Register a view.

        :param target: view function or view class.
        :param endpoint: (optional) endpoint name.
        :param blueprint: (optional) blueprint name.
        :param tuple resource_class_args: (optional) args to be forwarded to the
            view class constructor.
        :param dict resource_class_kwargs: (optional) kwargs to be forwarded to
            the view class constructor.
        """
        if isinstance(target, types.FunctionType):
            paths = self.view_converter.convert(target, endpoint, blueprint)
        elif isinstance(target, ResourceMeta):
            paths = self.resource_converter.convert(
                target,
                endpoint,
                blueprint,
                resource_class_args=resource_class_args,
                resource_class_kwargs=resource_class_kwargs,
            )
        else:
            raise TypeError()
        for path in paths:
            self.spec.path(**path, app=self.app)


def marshal_with(schema, code='default', description='', inherit=None, apply=None):
    """Marshal the return value of the decorated view function using the
    specified schema.

    Usage:

    .. code-block:: python

        class PetSchema(Schema):
            class Meta:
                fields = ('name', 'category')

        @marshal_with(PetSchema)
        def get_pet(pet_id):
            return Pet.query.filter(Pet.id == pet_id).one()

    :param schema: :class:`Schema <marshmallow.Schema>` class or instance, or `None`
    :param code: Optional HTTP response code
    :param description: Optional response description
    :param inherit: Inherit schemas from parent classes
    :param apply: Marshal response with specified schema
    """
    def wrapper(func):
        options = {
            code: {
                'schema': schema or {},
                'description': description,
            },
        }
        annotate(func, 'schemas', [options], inherit=inherit, apply=apply)
        # add custom wrapper
        annotate(func, 'wrapper', [{'wrapper': _CustomWrapper}])
        return activate(func)
    return wrapper


class _CustomWrapper(Wrapper):
    def __call__(self, *args, **kwargs):
        response = self.call_view(*args, **kwargs)
        if isinstance(response, wrappers.Response):
            return response
        rv, status_code, headers = unpack(response)
        if isinstance(rv, str):
            return response
        if isinstance(rv, wrappers.Response):
            return response

        mv = self.marshal_result(rv, status_code)
        mv = flask.jsonify({'code': response_util.RetCodeAndMessage.Base, 'data': mv, 'msg': '成功'})
        response = packed(mv, status_code, headers)
        return flask.current_app.make_response(response)
