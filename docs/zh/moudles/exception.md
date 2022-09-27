# 说明

异常模块，主要用于序列化器或者视图中检验数据错误等操作直接返回指定的报错信息

使用方法：

```python
raise ValidationException(ResponseStatus.VALIDATION_ERROR)
```



