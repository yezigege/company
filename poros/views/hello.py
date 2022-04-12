from ctypes import util


from util.blueprint import RootBlueprint


hello_bp = RootBlueprint('hello', __name__,  url_prefix='/hello')


@hello_bp.route('/', methods=['GET'])
def hello():
    return "Hello Views"
