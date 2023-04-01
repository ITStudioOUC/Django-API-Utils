# 说明

认证模块，基于`djangorestframework-simplejwt`，但原认证模块`username`和`password`字段为必传，故进行了封装，摆脱这种限制并附带了一些其他功能。

## simplejwt的配置

在`settings.py`中配置

```python
SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), # refresh_token有效时长
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30), # access_token有效时长
    'ROTATE_REFRESH_TOKENS': True, # refresh_token刷新时能否被刷新
}
```

## Token的获取

在路由中进行如下配置

```python
from it_drf_utils.auth import ITTokenRefreshView, ITTokenObtainPairView
urlpatterns = [
    # 用于获取token
	path(r"login/", ITTokenObtainPairView.as_view(), name='token_obtain_pair'),
	# 用于刷新token
    path(r"refresh/", ITTokenRefreshView.as_view(), name='token_refresh'),
]
```

关于Token有三个类`ITTokenObtainPairView`,`ITTokenRefreshView`,`ITTokenVerifyView`分别对应着获取、刷新、可用检测三个功能，可以点进`auth.py`进行查看

## Token的使用

发送请求时，在header内携带`Authorization`头，内容为`Bearer token`，Bearer为rest_framework_simplejwt默认配置的，你如果不想使用这个前缀，可以自行配置`'AUTH_HEADER_TYPES'`

```python
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',)
}
```

## 认证的使用

在`view.py`的各个`ViewSetPlus`中设置自己的认证组件

```python
class SampleView(ViewSetPlus):
    base_url_path = "/"
    # 设置认证组件
    authentication_classes = [JWTTokenUserAuthentication, ]
    
    # 如果一定要认证才能查看，可以查询DRF的权限认证组件
    permission_classes = (IsAuthenticated,)
    
    @get_mapping(value="sample")
    def sample(self,request,*args,**kwgs):
        user = requset.user # 这样即可获取到认证的TokenUser类，注意与User类不一样！！！
        # 如果为ITTokenUser，可用to_model()转化为对象，参考下面介绍
        user = request.user.to_mdoel()
```

如果你想默认所有接口都认证，可以在`settings.py`中配置默认的认证组件，这样就不用在各个View中都写一遍了，同理权限组件也可以设置

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    )
}
```

认证组件中的TokenUser类不能直接获取到User对象，比较麻烦，于是继承了一个`ITJWTTokenUserAuthentication`类，新增了`to_model()`方法，可以直接获取到User对象，使用前需要在`settings.py`中配置`ITAUTH_USER_MODEL`

```python
ITAUTH_USER_MODEL = "user.User"
# 格式为: app_name.label_name 例：user.User 无需写成user.models.User
```

如果你想默认使用`ITTokenUser`可以在`settings.py`的`SIMPLE_JWT`中配置

```python
SIMPLE_JWT = {
    'TOKEN_USER_CLASS': 'it_drf_utils.auth.ITTokenUser'
}
```

## 自定认证Model

如果你不想使用Django自带的user model，你也可以自定义认证后台

```python
AUTHENTICATION_BACKENDS = (
    # 和普通类的定位一样 app_name.file_name.class_name
    'user.authentication.MyCustomBackend',
)
```

类的写法

```python
from django.contrib.auth.backends import ModelBackend
class MyCustomBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        data = request.data
        .....
        
        # 认证成功返回User对象，失败返回None即可
        # 可参考写法
        try:
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            if user.password == password:
                return user
        except Exception as e:
            return None

```

## 豁免CSRF的Session认证
认证组件使用`csrfExemptAuth.py`中的`CsrfExemptSessionAuthentication`

并在`settings.py`中配置`CSRF_EXEMPT_PATH_LIST`，内容为需要豁免CSRF的路径，例如:`/blog/list`。

如果数组内容为`['all']`或者未配置，则所有使用该认证的免于CSRF认证

## 附录

1. simplejwt的默认配置

   ```python
   DEFAULTS = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
       'ROTATE_REFRESH_TOKENS': False,
       'BLACKLIST_AFTER_ROTATION': False,
       'UPDATE_LAST_LOGIN': False,
   
       'ALGORITHM': 'HS256',
       'SIGNING_KEY': settings.SECRET_KEY,
       'VERIFYING_KEY': None,
       'AUDIENCE': None,
       'ISSUER': None,
       'JWK_URL': None,
       'LEEWAY': 0,
   
       'AUTH_HEADER_TYPES': ('Bearer',),
       'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
       'USER_ID_FIELD': 'id',
       'USER_ID_CLAIM': 'user_id',
       'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
   
       'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
       'TOKEN_TYPE_CLAIM': 'token_type',
   
       'JTI_CLAIM': 'jti',
       'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
   
       'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
       'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
       'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
   }
   ```

2. rest_framework默认配置

   ```python
   DEFAULTS = {
       # Base API policies
       'DEFAULT_RENDERER_CLASSES': [
           'rest_framework.renderers.JSONRenderer',
           'rest_framework.renderers.BrowsableAPIRenderer',
       ],
       'DEFAULT_PARSER_CLASSES': [
           'rest_framework.parsers.JSONParser',
           'rest_framework.parsers.FormParser',
           'rest_framework.parsers.MultiPartParser'
       ],
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.SessionAuthentication',
           'rest_framework.authentication.BasicAuthentication'
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.AllowAny',
       ],
       'DEFAULT_THROTTLE_CLASSES': [],
       'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
       'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
       'DEFAULT_VERSIONING_CLASS': None,
   
       # Generic view behavior
       'DEFAULT_PAGINATION_CLASS': None,
       'DEFAULT_FILTER_BACKENDS': [],
   
       # Schema
       'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
   
       # Throttling
       'DEFAULT_THROTTLE_RATES': {
           'user': None,
           'anon': None,
       },
       'NUM_PROXIES': None,
   
       # Pagination
       'PAGE_SIZE': None,
   
       # Filtering
       'SEARCH_PARAM': 'search',
       'ORDERING_PARAM': 'ordering',
   
       # Versioning
       'DEFAULT_VERSION': None,
       'ALLOWED_VERSIONS': None,
       'VERSION_PARAM': 'version',
   
       # Authentication
       'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
       'UNAUTHENTICATED_TOKEN': None,
   
       # View configuration
       'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
       'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',
   
       # Exception handling
       'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
       'NON_FIELD_ERRORS_KEY': 'non_field_errors',
   
       # Testing
       'TEST_REQUEST_RENDERER_CLASSES': [
           'rest_framework.renderers.MultiPartRenderer',
           'rest_framework.renderers.JSONRenderer'
       ],
       'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',
   
       # Hyperlink settings
       'URL_FORMAT_OVERRIDE': 'format',
       'FORMAT_SUFFIX_KWARG': 'format',
       'URL_FIELD_NAME': 'url',
   
       # Input and output formats
       'DATE_FORMAT': ISO_8601,
       'DATE_INPUT_FORMATS': [ISO_8601],
   
       'DATETIME_FORMAT': ISO_8601,
       'DATETIME_INPUT_FORMATS': [ISO_8601],
   
       'TIME_FORMAT': ISO_8601,
       'TIME_INPUT_FORMATS': [ISO_8601],
   
       # Encoding
       'UNICODE_JSON': True,
       'COMPACT_JSON': True,
       'STRICT_JSON': True,
       'COERCE_DECIMAL_TO_STRING': True,
       'UPLOADED_FILES_USE_URL': True,
   
       # Browseable API
       'HTML_SELECT_CUTOFF': 1000,
       'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",
   
       # Schemas
       'SCHEMA_COERCE_PATH_PK': True,
       'SCHEMA_COERCE_METHOD_NAMES': {
           'retrieve': 'read',
           'destroy': 'delete'
       },
   }
   ```

   
