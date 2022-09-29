# 说明

异常模块，主要用于序列化器或者视图中检验数据错误等操作直接返回指定的报错信息

使用方法：

```python
raise ValidationException(ResponseStatus.VALIDATION_ERROR)
```

## 样例

### 序列化器样例

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def validate(self, attrs):
        if not re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', attrs['email']):
            raise ValidationException(ResponseStatus.VALIDATION_ERROR)
        return attrs
```

### 视图（View）

```python
class ArticleView(ViewSetPlus):
    base_url_path = "/"

    @get_mapping(value="article/detail")
    def get_single_article(self, request, *args):
        article_id = request.GET.get('id', '')
        article = Article.objects.filter(article_id=article_id, article_type=0)
        if not article.exists():
            raise ValidationException(ResponseStatus.NOT_EXIST_ERROR)
        serializer = ArticleSerializer(article.first())
        return Response(ResponseStatus.OK, serializer.data)
```

