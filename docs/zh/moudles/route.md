# 说明

路由基于`djangorestframework`的`SimpleRouter`进行修改。

可以自动化收集 View 中的类并根据 `base_url_path`, `base_url_name` 生成对应的 URL
使用时要求符合以下规范:

       1. 所有的 app 放在 'apps' 目录下, 该目录和项目在根目录下
       2. 如果不设置 `base_url_path`, `base_url_name`, `url_pattern` 的值, 会默认使用类名的小写字母作为默认值

## 设置路由

在项目的`urls.py`文件中，设置路由，代码如下

```python
from django.urls import path, include
from utils.router_builder import RouterBuilder

router = RouterBuilder()
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(router.url_patterns))
]
```

此时会根据apps目录下的各个app的views.py文件生成路由。

如果需要根据非views文件生成路由，可以使用使用collect函数，`router.collect(app_name,file_name)`

```python
from django.urls import path, include
from autils.router_builder import RouterBuilder

router = RouterBuilder()
router.collect('user', 'team')  # 根据apps/user/team.py文件生成路由
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(router.url_patterns))
]
```

### trailing_slash

是否需要以`/`作为路由的结尾，默认为True

如果以`/`做为路由结尾，则url地址为`https://domain/user/info/`，如果使用`https://domain/user/info`会报404错误

## mapping

效仿 Spring 的注解, 基于 @action 封装了一些更加常用装饰器，用于`ViewSetPlus`

1. @get_mapping

2. @post_mapping

3. @put_mapping

4. @delete_mapping

!> 不要将一个 URL 的同一种请求(GET, POST)映射到两个不同的函数上，用APIViewPlus替代


## 使用示例

### urls.py

```python
from django.urls import path, include
from autils.router_builder import RouterBuilder

router = RouterBuilder()
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(router.url_patterns))
]
```

### views.py

```python
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
```

即可生成如下效果的url

```python
urlpatterns = [
    path("api/blog/add/", addBlog, name="blog-addBlog"),
    path("api/blog/search/", getBlog, name="blog-getBlog"),
    path("api/blog/test/", BlogTester.as_view(), name="blogtester")
]
```

