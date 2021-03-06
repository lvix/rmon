from functools import wraps

from flask import g

from rmon.common.rest import RestException


class ObjectMustExist:
    """该装饰器确保对象存在
    """

    def __init__(self, object_class):
        """
        object_class: 数据库对象
        """
        self.object_class = object_class

    def __call__(self, func):
        """
        装饰器实现
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Args: 
                object_id(int): SQLAlchemy object id
            """
            object_id = kwargs.get('object_id')
            if object_id is None:
                raise RestException(404, 'object doesn\'t exist')

            obj = self.object_class.query.get(object_id)
            if obj is None:
                raise RestException(404, 'object doesn\'t exist')
            g.instance = obj
            return func(*args, **kwargs)

        return wrapper
