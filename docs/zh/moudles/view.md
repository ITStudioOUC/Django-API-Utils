# 说明

视图层我们封装了两个类，`ViewSetPlus`和`APIViewPlus`，其中：

`ViewSetPlus`用于多个url，多种请求方式。

`APIViewPlus`用于同一个url，不同请求方式。

!> APIViewPlus的情况ViewSetPlus处理不了

# ViewSetPlus

#### params:

| 参数          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| base_url_path | URL 根路径, 所有 ViewSet 下 mapping 修饰器都会自动在 URL 最开始增加该路径<br />如果为空则默认使用类名的小写！ |
| base_url_name | URL 的别名, 用于后端跳转场景，如果为空则默认使用类名的小写！ |
| url_pattern   | 在 `urlpatterns` 中注册使用的 URL 匹配路径，<b>`as_api_view=True`才可用</b> |
| as_api_view   | 接口注册 URL 的形式          (默认为False)<br /> True: 以 APIView 的形式在 `urlpatterns` 中添加<br />False: 在 drf 的 router 里注册 |

#### 使用示例：

```python
from rest_framework.parsers import JSONParser
from autils.api_view import ViewSetPlus
from autils.mapping import post_mapping, get_mapping
from autils.response import Response
from autils.response_status import ResponseStatus


class BlogController(ViewSetPlus):
    base_url_name = "blog"
    base_url_path = "blog"

    @post_mapping(value="add")
    def addBlog(self, request, *args, **kwargs):
        api_data = request.data
        serializer = BlogSerializer(data=api_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(ResponseStatus.OK)

    @get_mapping(value="search")
    def getBlog(self, request, *args, **kwargs):
        queryset = Blog.objects.all()
        serializers = BlogSerializer(queryset, many=True)
        return Response(ResponseStatus.OK, serializers.data)
```

# APIViewPlus

是`ViewSetPlus`的继承

#### params

| 参数        | 说明                                       |
| ----------- | ------------------------------------------ |
| url_pattern | 在 `urlpatterns` 中注册使用的 URL 匹配路径 |
| as_api_view | 默认为True，<b>禁止修改！</b>              |

#### 使用示例

```python
from autils.api_view import APIViewPlus
from autils.response import Response
from autils.response_status import ResponseStatus


class BlogController(APIViewPlus):

    def get(self, request, *args, **kwargs):
        ....
        return Response(ResponseStatus.OK)

    def post(self, request, *args, **kwargs):
        ....
        return Response(ResponseStatus.OK)
```

# Response

Response基于django的`HttpResponse`修改，返回json页面。

```python
Response(ResponseStatus.xxx, data)
```

### ResponseStatus

响应状态的枚举类，继承自Enum，用于确定返回的`code`和`msg`。

成功的示例为：

```python
OK = (20000, '成功')
```

### data（可选参数）<!-- {docsify-ignore} -->

返回的数据，如果为None或者空字典则不显示。

!> 只有ResponseStatus.OK时可用，其他错误信息会默认忽略掉data

### 使用示例 <!-- {docsify-ignore} -->

1. 成功示例

```python
Response(ResponseStatus.OK, {'username':'admin'})
```

返回页面为:

```json
{
    "code": 20000,
    "msg": "成功",
    "data": {
        "username": "admin"
    }
}
```

2. 失败示例

```python
Response(ResponseStatus.UNEXPECTED_ERROR)
```

返回页面为：

```json
{
    "code": 50000,
    "msg": "意外错误"
}
```

# 关于交互时数据解析Parser的说明

对于前后端数据的交互数据获取问题

关于`POST` , `PUT`, `DELETE`等方法获取数据建议：

1. 先在`settings.py`文件中配置

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PARSER_CLASSES': (
           'rest_framework.parsers.JSONParser',  # application/json
           'rest_framework.parsers.FormParser',  # application/x-www-form-urlencoded
           'rest_framework.parsers.MultiPartParser', # multipart/form-data
       )
   }
   ```

2. 之后在`view`中使用`request.data`获取数据

关于`GET`方法获取数据

建议使用`request.query_params`而不是`request.GET`，一点是语义更精准，另一点是不用大小写来回切换，总的来说就是优雅。
