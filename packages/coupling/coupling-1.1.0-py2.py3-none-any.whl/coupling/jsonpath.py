# coding: utf-8

import inspect
import typing
from jsonpath_ng.ext import parse


Empty = inspect.Parameter.empty


class NotFoundError(Exception):
    pass


def search(path: str, data: typing.Union[list, dict], default=Empty,
           smart_unique: bool = True) -> typing.Union[int, float, bool, str, list, dict, None]:
    """
    when not found:
    if raise_not_found is true, raise NotFoundError, else return default value.
    """
    expr = parse(path)
    resp = expr.find(data)

    if not resp:
        if default is Empty:
            raise NotFoundError("Can't find by path: {}".format(path))
        else:
            return default

    if len(resp) == 1 and smart_unique:
        return resp[0].value
    else:
        return [match.value for match in resp]


search.NotFoundError = NotFoundError
