from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .exception import ValidationException
from .response import ResponseStatus



class ITModelSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=True):
        """
        重写了一下，使序列化器验证的字段错误可以优雅地引发第一个报错。
        :param raise_exception: 是否引发异常
        """
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            for i in iter(self._errors.values()):
                try:
                    raise ValidationException(ResponseStatus[i[0]])
                except KeyError:
                    pass
            raise ValidationError(self.errors)

        return not self._errors
