from . import exceptions
from enum import Enum, auto


class FieldException(exceptions.PrintableException):
    pass


def clean(field):
    # TODO Add docs

    from functools import wraps

    if not isinstance(field, Field):
        raise TypeError("Expected Field")

    def decorator(func):

        @wraps(func)
        def wrappedFunc(data):

            try:
                data = field.clean(data)
                return func(data)
            except FieldException as e:
                raise exceptions.BadRequestException("Request validation error") from e

        return wrappedFunc

    return decorator


class Do(Enum):
    # TODO Add docs
    SKIP = auto(),
    RAISE = auto()


class Default:
    # TODO Add docs

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class Field:
    # TODO Add docs

    def __init__(self, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        if not isinstance(missing, (Do, Default)):
            raise TypeError("Expected missing action")
        if not isinstance(error, (Do, Default)):
            raise TypeError("Expected error action")
        self._missing = missing
        self._error = error

    @property
    def onMissing(self):
        return self._missing

    @property
    def onError(self):
        return self._error

    def clean(self, value):
        # TODO Add docs
        raise NotImplementedError()

    def cleanAndAdd(self, present, value, add):
        # TODO Add docs
        if present:
            try:
                value = self.clean(value)
            except FieldException as e:
                if self._error == Do.RAISE:
                    raise e
                elif isinstance(self._error, Default):
                    add(self._error.value)
            else:
                add(value)
        else:
            if self._missing == Do.RAISE:
                raise FieldException("Required but missing")
            elif isinstance(self._missing, Default):
                add(self._missing.value)


class TypeField(Field):
    # TODO Add docs

    def __init__(self, type, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(missing=missing, error=error)
        self._type = type

    @property
    def type(self):
        return self._type

    @staticmethod
    def formatTypeConstraint(typeConstraint):
        if isinstance(typeConstraint, type):
            return typeConstraint.__name__
        elif isinstance(typeConstraint, (tuple, list)):
            return " or ".join(map(lambda t: t.__name__, typeConstraint))
        else:
            return "<error type>"

    def clean(self, value):
        if not isinstance(value, self._type):
            raise FieldException(f"Expected type {TypeField.formatTypeConstraint(self._type)}")
        return value


class ScalarField(TypeField):
    # TODO Add docs

    def __init__(self, type, min=None, max=None, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(type, missing=missing, error=error)
        self._min = min
        self._max = max

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def clean(self, value):
        value = super().clean(value)
        if self._min is not None and value < self._min:
            raise FieldException(f"Value must be >= {self._min}")
        if self._max is not None and value > self._max:
            raise FieldException(f"Value must be <= {self._max}")
        return value


class IntField(ScalarField):
    # TODO Add docs

    def __init__(self, min=None, max=None, missing=Do.RAISE, error=Do.RAISE):
        super().__init__(int, min=min, max=max, missing=missing, error=error)


class FloatField(ScalarField):
    # TODO Add docs

    def __init__(self, min=None, max=None, missing=Do.RAISE, error=Do.RAISE):
        super().__init__((int, float), min=min, max=max, missing=missing, error=error)


class BoolField(TypeField):
    # TODO Add docs

    def __init__(self, missing=Do.RAISE, error=Do.RAISE):
        super().__init__(bool, missing=missing, error=error)


class StringField(TypeField):
    # TODO Add docs

    def __init__(self, minLength=None, maxLength=None, regex=None, missing=Do.RAISE, error=Do.RAISE):
        super().__init__(str, missing=missing, error=error)
        self._minLength = minLength
        self._maxLength = maxLength
        import re
        self._regex = re.compile(regex) if regex is not None else None

    @property
    def minLength(self):
        return self._minLength

    @property
    def maxLength(self):
        return self._maxLength

    @property
    def regex(self):
        return self._regex

    def clean(self, value):
        value = super().clean(value)
        if self._minLength is not None and len(value) < self._minLength:
            raise FieldException(f'String must be at least {self._minLength} characters long')
        if self._maxLength is not None and len(value) > self._maxLength:
            raise FieldException(f'String cannot be longer than {self._maxLength} characters')
        if self._regex is not None and not self._regex.match(value):
            raise FieldException(f'String does not match regex "{self._regex}"')
        return value


class ListField(TypeField):
    # TODO Add docs

    def __init__(self, minLength=None, maxLength=None, fields=None, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(list, missing=missing, error=error)
        self._minLength = minLength
        self._maxLength = maxLength
        self._fields = fields

    @property
    def minLength(self):
        return self._minLength

    @property
    def maxLength(self):
        return self._maxLength

    @property
    def fields(self):
        return self._fields

    def clean(self, value):
        value = super().clean(value)
        if self._minLength is not None and len(value) < self._minLength:
            raise FieldException(f'List length must be >= {self._minLength}')
        if self._maxLength is not None and len(value) > self._maxLength:
            raise FieldException(f'List length must be <= {self._maxLength}')
        if self._fields is not None:
            if isinstance(self._fields, list):
                fields = self._fields
            elif isinstance(self._fields, Field):
                fields = [self._fields] * len(value)
            else:
                raise TypeError("Bad type fields type")
            items = []
            for i, item in enumerate(value):
                if fields[i] is not None:
                    try:
                        fields[i].cleanAndAdd(True, item, items.append)
                    except FieldException as e:
                        raise FieldException(f"Field exception on item {i}") from e
                else:
                    items.append(item)
            value = items
        return value

    @staticmethod
    def byLength(length, fields=None, missing=Do.RAISE, error=Do.RAISE):
        return ListField(length, length, fields, missing, error)

    @staticmethod
    def byFields(fields=None, missing=Do.RAISE, error=Do.RAISE):
        return ListField.byLength(len(fields), fields, missing, error)


class TimeField(TypeField):
    # TODO Add docs

    def __init__(self, min=None, max=None, tzAware=None, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(str, missing=missing, error=error)
        self._min = min
        self._max = max
        self._tzAware = tzAware

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def timezoneAware(self):
        return self._tzAware

    def clean(self, value):
        try:
            from dateutil import parser
            value = parser.parse(value)
        except ValueError as e:
            raise FieldException(f"Invalid datetime: {e}")
        except OverflowError as e:
            raise FieldException("Overflow error")
        if self._min is not None and value < self._min:
            raise FieldException(f"Value must be >= {self._min}")
        if self._max is not None and value > self._max:
            raise FieldException(f"Value must be <= {self._max}")
        if self._tzAware is not None:
            if self._tzAware != (value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None):
                raise FieldException(f"Value must {'' if self._tzAware else 'not '}be timezone aware")
        return value


class DictField(TypeField):
    # TODO Add docs

    def __init__(self, fields=None, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(dict, missing=missing, error=error)
        self._fields = fields

    @property
    def fields(self):
        return self._fields

    def clean(self, value):
        value = super().clean(value)
        if self._fields is not None:
            dictionary = {}
            if isinstance(self._fields, Field):
                for key, item in value.items():
                    try:
                        def add(v):
                            dictionary[key] = v
                        self._fields.cleanAndAdd(True, item, add)
                    except FieldException as e:
                        raise FieldException(f'Field exception on item "{key}"') from e
            elif isinstance(self._fields, dict):
                for key, item in self._fields.items():
                    try:
                        def add(v):
                            dictionary[key] = v
                        present = key in value
                        self._fields[key].cleanAndAdd(present, value[key] if present else None, add)
                    except FieldException as e:
                        raise FieldException(f'Field exception on item "{key}"') from e
                unexpected = set(value.keys()) - set(self._fields.keys())
                if len(unexpected) > 0:
                    raise FieldException(f'Unexpected fields {unexpected}')
            else:
                raise TypeError("Bad fields type")
            value = dictionary
        return value


class OptionField(Field):
    # TODO Add docs

    def __init__(self, field, options, missing=Do.RAISE, error=Do.RAISE):
        # TODO Add docs
        super().__init__(missing=missing, error=error)
        if not isinstance(field, Field):
            raise TypeError("Expected Field type")
        if not isinstance(options, list):
            raise TypeError("Expected list type")
        self._field = field
        self._options = options

    @property
    def field(self):
        return self._field

    @property
    def options(self):
        return self._options.copy()

    def clean(self, value):
        v = self._field.clean(value)
        if v not in self._options:
            def strfy(x):
                return f'"{x}"' if isinstance(x, str) else str(x)
            raise FieldException(f"Expected {' or '.join(map(strfy,self._options))}")
        return v
