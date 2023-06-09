
class RedisKeyPrefix:
    #redis键值前缀，所有键值都在这定义
    cache_api = 'cache_api'



class MyException(Exception):
    #自定义错误码，所有错误码都在这定义
    def __init__(self, e):
        self.code, self.error = e
    def __str__(self):
        return self.error
    error = 1, '未知异常'
    nopermission = 2, '权限不足'
    nologin = 100, '未登入'
    timeout = 101, '超时'
    login = 102, '登入失败'

RKP = RedisKeyPrefix
ME = MyException

from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse, HttpResponse, StreamingHttpResponse
from django.core.exceptions import PermissionDenied
from functools import wraps
import logging


class ViewsMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        #调用视图前被调用
        if getattr(view, 'login_exempt', False):
            return None
        if not request.user.is_authenticated:
            return JsonResponse({'code': ME.nologin[0], 'message': ME.nologin[1]})

    def process_response(self, request, response):
        # 视图函数返回时调用
        if isinstance(response, (JsonResponse, HttpResponse, StreamingHttpResponse)):
            return response
        else:
            return JsonResponse({'code': 0, 'data': response, 'message': ''})

    def process_exception(self, request, exception):
        # 视图函数发生异常时调用
        logging.getLogger('log').exception(exception)
        if isinstance(exception, ME):
            code, exception = exception.code, exception.error
        elif isinstance(exception, (PermissionDenied,)):
            code, exception = ME.nopermission
        else:
            code, exception = ME.error[0], str(exception) or ME.error[1]
        return JsonResponse({'code': code, 'message': exception})

def login_exempt(view_func):
    #免登入装饰器，在中间件中已默认所有接口登入
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.login_exempt = True
    return wraps(view_func)(wrapped_view)