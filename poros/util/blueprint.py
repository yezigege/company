from flask import Blueprint


class RootBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        if 'url_prefix' in kwargs:
            kwargs['url_prefix'] = '/service' + kwargs['url_prefix']
        super(RootBlueprint, self).__init__(*args, **kwargs)
