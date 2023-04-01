from enum import Enum


class ResponseStatus(Enum):
    """
    响应状态的枚举类

    状态类型格式形如:
    STATUS_NAME = (code: int, message: str)

    Example:
        OK = (20000, '成功')
    """

    OK = (20000, '成功')

    UNEXPECTED_ERROR = (50000, '意外错误')

    CSRF_FAILED_ERROR = (50001, 'CSRF认证失败')

    METHOD_NOT_ALLOWED_ERROR = (40000, '请求方法错误')

    VALIDATION_ERROR = (40001, '数据格式错误')

    AUTH_FAILED_ERROR = (40002, '用户认证失败')

    TOKEN_ERROR = (40002, 'token不合法或已过期')

    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]
