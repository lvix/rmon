""" rmon.rmon.rest
"""
from collections import Mapping
from flask import request, Response, make_response
from flask.json import dumps
from flask.views import MethodView


class RestException(Exception):
    """exception base
    """

    def __init__(self, code, message):
        """
        init exception 

        Aargs:
            code (int): http status code 
            message (str): error info 
        """

        self.code = code
        self.message = message
        super(RestException, self).__init__()


class RestView(MethodView):
    """ customized View class
        json serialization, exception catch, decorators
        """
    content_type = 'application/json; charset=utf-8'
    method_decorators = []

    def handler_error(self, exception):
        """exceptions
        """
        data = {
            'ok': False,
            'message': exception.message
        }

        result = dumps(data) + '\n'
        resp = make_response(result, exception.code)
        resp.headers['Content-Type'] = self.content_type
        return resp

    def dispatch_request(self, *args, **kwargs):
        """重写父类方法，支持数据自动序列化
        """

        # 如果直接使用 self.method , 如果方法不存在会报错，而 getattr 可以避免这个问题
        method = getattr(self, request.method.lower(), None)
        if method is None and request.method == 'HEAD':
            method = getattr(self, 'get', None)

        assert method is not None, 'Uninplemented method {}'.format(request.method)

        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            method = decorator(method)

        try:
            resp = method(*args, **kwargs)
        except RestException as e:
            resp = self.handler_error(e)

        # 如果返回结果已经是 HTTP 响应则直接返回
        if isinstance(resp, Response):
            return resp

        # 从返回值中解析出 HTTP 响应信息，比如状态码和头部
        data, code, headers = RestView.unpack(resp)

        # 处理错误，HTTP 状态码大于 400 时认为是错误
        # 返回的错误类似于 {'name':['Redis server already exist']}
        # 将其调整为 {'ok': False, 'message': 'redis server already exist'}

        if code >= 400 and isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list) and len(data[key]) > 0:
                    message = data[key][0]
                else:
                    message = data[key]

            data = {'ok': False, 'message': message}

            # 序列化数据
            result = dumps(data) + '\n'

            # 生成 HTTP 响应
            response = make_response(result, code)
            response.headers.extend(headers)

            # 设置响应头为 application/json
            response.headers['Content-Type'] = self.content_type

            return response

        @staticmethod
        def unpack(value):
            """ 解析视图方法返回值
            """
            headers = {}
            if not isinstance(value, tuple):
                return value, 200, {}

            # 如果返回值有 3
            if len(value) == 3:
                data, code, headers = value
            elif len(value) == 2:
                data, code = value
            return data, code, headers
