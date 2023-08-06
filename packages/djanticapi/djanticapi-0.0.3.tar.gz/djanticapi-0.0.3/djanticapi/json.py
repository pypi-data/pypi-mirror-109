import decimal
import functools
from typing import Any, Callable, Union

import orjson
from django.db.models.query import QuerySet
from django.utils.encoding import force_str
from django.utils.functional import Promise
from pydantic import BaseModel

from djanticapi.form import BaseFormModel
from djanticapi.exceptions import BaseAPIException


def default_encoder(obj):
    if isinstance(obj, BaseAPIException):
        return obj.__dict__
    if isinstance(obj, QuerySet):
        return tuple(obj)
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, (BaseFormModel, BaseModel)):
        return obj.dict()
    # For Date Time string spec, see ECMA 262
    # https://ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
    if isinstance(obj, Promise):
        return force_str(obj)
    if not isinstance(obj, dict) and hasattr(obj, '__getitem__'):
        try:
            return dict(obj)
        except Exception:
            pass
    if not isinstance(obj, (list, tuple)) and hasattr(obj, '__iter__'):
        return tuple(item for item in obj)


@functools.wraps(orjson.dumps)
def dumps(obj: Any, default: Callable[[Any], Any] = None, **kwargs) -> bytes:
    if default is None:
        default = default_encoder
    return orjson.dumps(obj, default=default, **kwargs)


@functools.wraps(orjson.loads)
def loads(obj: Union[bytes, bytearray, memoryview, str]) -> Any:
    return orjson.loads(obj)
