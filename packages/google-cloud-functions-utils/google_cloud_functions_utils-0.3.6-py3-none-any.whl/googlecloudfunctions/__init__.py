from flask import jsonify

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600'
}


class _HttpWrapper:
    def __init__(self, request):
        self.request = request

    def send_response(self, result):
        return (jsonify(result[0]), result[1], HEADERS)


class ClientWrapper:
    def __init__(self, client, *args, **kwargs):
        self.template_client = client
        self.arguments = args
        self.kw_arguments = kwargs
        self.create_client()

    def create_client(self):
        self.client = self.template_client(*self.arguments, **self.kw_arguments)

    def execute(self, f, *args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except Exception as exc:
            self.create_client()
            response = getattr(self.client, f.__name__)(*args, **kwargs)
        return response


def gcf(func):
    def wrapper(*args):
        if args[0].method == 'OPTIONS':
            return (jsonify(''), 204, HEADERS)
        try:
            result = func(args[0])
        except Exception as error:
            return (jsonify({'error': str(error)}), 500, HEADERS)
        return _HttpWrapper(args[0]).send_response(result)

    return wrapper
