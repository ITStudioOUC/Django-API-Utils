from rest_framework.exceptions import MethodNotAllowed

from utils.response import Response
from utils.response_status import ResponseStatus
from utils.exception import ValidationException
from rest_framework.viewsets import ViewSet


class ViewSetPlus(ViewSet):
    """
    增强 ViewSet 的功能, 增加 URL 的定义相关字段和自定义的异常类型
    :param base_url_path: URL 根路径, 所有 ViewSet 下 mapping 修饰器都会自动在 URL 最开始增加该路径
    :param base_url_name: URL 的别名, 用于后端跳转场景
    :param as_api_view: 接口注册 URL 的形式,
                          True: 以 APIView 的形式在 `urlpatterns` 中添加
                          False: 在 drf 的 router 里注册
    :param url_pattern: 在 `urlpatterns` 中注册使用的 URL 匹配路径
    """
    base_url_path = ""
    base_url_name = ""
    as_api_view = False
    url_pattern = ""

    def handle_exception(self, exc) -> Response:
        """
        对异常的处理函数进行封装, 打印异常信息并给前端返回对应的提示信息
        :param exc: 异常
        :return Response: 自定义的返回类, 见 utils.response.Response
        """
        # TODO:添加错误信息显示在控制台或者使用日志记录
        # print(exc)
        # logger.error(exc)
        if isinstance(exc, MethodNotAllowed):
            return Response(ResponseStatus.METHOD_NOT_ALLOWED_ERROR)

        if isinstance(exc, ValidationException):
            return Response(exc.status)

        return Response(ResponseStatus.UNEXPECTED_ERROR)


class APIViewPlus(ViewSetPlus):
    """
    支持 APIView 的写法, 实现默认的 get, post, delete, put 处理函数便于 URL的绑定
    """
    as_api_view = True

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="GET")

    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="POST")

    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="DELETE")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="PUT")
