# 项目说明

Django-API-Utils是基于Django编写后端API的一些组件和工具，致力于努力探究 Django 最佳实践。

目前基于 [ITM-0011](https://github.com/ITStudioOUC/ITM/blob/main/documents/ITM-0011.txt) 中的规范编写，仍待完善和在实践中优化。

# 环境依赖

目前已在 Django 3 下测试可以成功运行。

环境要求：

`Django >= 3.2`, `djangorestframework >= 3.12` , `djangorestframework-simplejwt >= 5.0.0`
（如果不使用认证组件，将auth.py删除即可，不必安装此模块）

# 初始化项目

1. 下载本项目源码，将utils文件夹拖到项目根目录下

   下载本项目源码可以使用git工具、直接在Github上Download ZIP、或者下载发布的release包。

2. 新建`apps`目录，将项目内的app放入apps文件夹内。

3. 在`settings.py`文件内，新增apps目录到`BASE_DIR`

   ```python
   ...
   BASE_DIR = Path(__file__).resolve().parent.parent
   # 新增下面这一行
   sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
   ...
   ```

4. 在根路由文件`urls.py`下初始化`Router Build`

   ```python
   from autils.router_builder import RouterBuilder
   router = RouterBuilder()
   urlpatterns = [
       path("api/", include(router.urls)),
       path("api/", include(router.url_patterns)),
   ]
   ```

5. （非必需）在项目根目录下新建`config.json`文件，将项目的一些配置信息和敏感信息写到json文件中，并在`settings.py`中读取

   ```python
   import json
   
   # Configuration File
   with open('./conf.json', 'r') as f:
       config = json.load(f)
   
   SECRET_KEY = config.get('SECRET_KEY','')
   
   MYSQL_DB_NAME = config.get('MYSQL_DB_NAME','')
   MYSQL_DB_USER = config.get('MYSQL_DB_USER','')
   MYSQL_DB_PASSWORD = config.get('MYSQL_DB_PASSWORD','')
   ```

   *这样的好处在于，避免将敏感信息暴露到Git服务器上。*

初始化完后，项目的目录树大概是这样的：

```
.
├── apps
│   ├── __init__.py
│   └── <app_name>
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   └── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       └── views.py
├── <project_name>
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── manage.py
└── config.json[可选]
```

# 使用教程

更多详细信息请参考[在线文档](https://itstudioouc.github.io/Django-API-Utils/)    
