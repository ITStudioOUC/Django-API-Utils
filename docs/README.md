# Django-API-Utils

基于Django编写后端API的一些组件和工具，致力于努力探究 Django 最佳实践。

基于 [ITM-0011](https://github.com/ITStudioOUC/ITM/blob/main/documents/ITM-0011.txt) 中的规范编写，仍待完善和在实践中优化。

## 依赖

目前已在 Django 3 下测试可以成功运行。

环境要求：

`Django >= 3.2`, `djangorestframework >= 3.12`

## api_view

提供了两个基于 `ViewSet` 类的封装，加入了 `base_url_path`, `base_url_name` 属性用于自动化收集并注册 API 的 URL，同时重载了处理异常函数，使得无论任何时候都可以正常返回。

使用示例:

```python
# views.py
class BlogController(ViewSetPlus):
    serializer_class = BlogSerializer
    base_url_name = "blog"
    base_url_path = "blog"

    @post_mapping(value="add")
    def addBlog(self, request, *args, **kwargs):
        api_data = JSONParser().parse(request)
        serializer = BlogSerializer(data=api_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(ResponseStatus.OK)

    @get_mapping(value="search")
    def getBlog(self, request, *args, **kwargs):
        queryset = Blog.objects.all()
        serializers = BlogSerializer(queryset, many=True)
        return Response(ResponseStatus.OK, serializers.data)

class BlogTester(APIViewPlus):
    url_pattern = "blog/test"
```

支持使用基于 router 装饰器的方法注册接口，所有被注册接口会拼上 `base_url_path`，同时也支持类似与 `APIView` 的写法，你需要手动的实现 `get`, `post`等方法，他们对应 URL 的同名请求。


## exception

自定义异常类，结合自定义枚举类 [ResponseStatus](#response_status) 使用。

使用示例：

```python
if expr<error>:
    raise ValidationException(ResponseStatus.<ERROR Enmu>)
```

## mapping

基于 `rest_framework.decorators.action` 的进一步封装，细分分为了`get_mapping`, `post_mapping`等，具体参考文件内的注释。

## response

实践 [ITM-0011](https://github.com/ITStudioOUC/ITM/blob/main/documents/ITM-0011.txt) 中提出的前后端数据交互规范。将返回格式固定为如下 json 格式：

```json
{
    "code": 20000,
    "msg": "OK",
    "data": {}
}
```

## response_status

实践 [ITM-0011](https://github.com/ITStudioOUC/ITM/blob/main/documents/ITM-0011.txt) 中提出的状态码和描述信息绑定的规范。结合自定义的 `Response`类和异常类，一致化 API 返回数据。

## router_builder

一个自动化收集视图类并绑定 URL 的方法，使用时在根目录（推荐）的 `urls.py`中声明：

该类将会收集 `views.py` 中所有继承 `ViewSetPlus` 和 `APIViewPlus` 的类自动在  `urls.py` 中注册。

```python
# views.py
class BlogController(ViewSetPlus):
    base_url_name = "blog"
    base_url_path = "blog"

    @post_mapping(value="add")
    def addBlog(self, request, *args, **kwargs):
        ......

    @get_mapping(value="search")
    def getBlog(self, request, *args, **kwargs):
        ......

class BlogTester(APIViewPlus):
    url_pattern = "blog/test"
    
    def post(self, request, *args, **kwargs):
        ......
    def get(self, request, *args, **kwargs):
        ......

# urls.py
router = RouterBuilder()
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(router.url_patterns)),
]
```

此时将会生成类似如下的结果：

```python
urlpatterns = [
    path("api/blog/add", addBlog, name="blog-addBlog"),
    path("api/blog/search", getBlog, name="blog-getBlog"),
    path("api/blog/test", BlogTester.as_view(), name="blogtester")
]
```

更多的信息参考文件内的文档描述。