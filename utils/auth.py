from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.apps import apps as django_apps
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt import serializers
from .response import Response
from .exception import ValidationException
from .response_status import ResponseStatus


class ITJWTTokenUserAuthentication(JWTTokenUserAuthentication):
    """
    继承JWTTokenUserAuthentication的一个认证组件，使request.user为ITTokenUser类型
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_user(self, validated_token):
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        return ITTokenUser(validated_token)


class ITTokenObtainPairSerializer(Serializer):
    """
    这是对rest_framework_simplejwt的一个重写，去除了原认证组件post信息内username和password为必填
    """

    def validate(self, attrs):
        authenticate_kwargs = {
            'request': self.context['request']
        } if 'request' in self.context.keys() else {}
        user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise ValidationException(ResponseStatus.AUTH_FAILED_ERROR)
        data = dict()
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class ITTokenViewBase(TokenViewBase):
    """
    TokenViewBase的包装类
    作为该工具的View试图基类，添加了异常处理，修改了token的返回格式为
    {
        "code": 20000,
        "msg": "成功",
        "data": {
            "refresh": "",
            "access": ""
        }
    }
    """

    def handle_exception(self, exc) -> Response:
        if isinstance(exc, AuthenticationFailed):
            return Response(ResponseStatus.TOKEN_ERROR)
        elif isinstance(exc, ValidationException):
            return Response(exc.status)
        elif isinstance(exc, MethodNotAllowed):
            return Response(ResponseStatus.METHOD_NOT_ALLOWED_ERROR)

        print(exc)
        return Response(ResponseStatus.UNEXPECTED_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(ResponseStatus.OK, serializer.validated_data)


class ITTokenObtainPairView(ITTokenViewBase):
    """
    返回refresh和access两种token的View
    """
    serializer_class = ITTokenObtainPairSerializer


class ITTokenRefreshView(ITTokenViewBase):
    """
    通过post请求使用refresh刷新access的View
    post data:
    {
        'refresh':''
    }
    返回：
    {
        'access':''
    }
    """
    serializer_class = serializers.TokenRefreshSerializer


class ITTokenVerifyView(ITTokenViewBase):
    """
    通过post请求检测access token是否可用
    post data:
    {
        'token':''
    }
    """
    serializer_class = serializers.TokenVerifySerializer


class ITTokenUser(TokenUser):
    """
    为TokenUser新增to_model，可以将TokenUser转化成User的model类
    如需使用需要在django的settings文件内新增ITAUTH_USER_MODEL字段，为字符串类型，
    格式为: app_name.label_name 例：user.User 无需写成user.models.User
    """

    def to_model(self):
        user_model = django_apps.get_model(settings.ITAUTH_USER_MODEL)
        user_str = f'user_model.objects.get({api_settings.USER_ID_FIELD}={self.id})'
        return eval(user_str)

    def __str__(self):
        return f'ITTokenUser {self.id}'
