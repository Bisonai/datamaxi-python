from typing import List
from urllib.parse import urlencode
import pandas as pd
from functools import wraps
from datamaxi.error import ParameterRequiredError
from datamaxi.error import AtLeastOneParameterRequiredError


def to_float(x):
    return float(x)


def to_int(x):
    return int(x)


def cleanNoneValue(d) -> dict:
    out = {}
    for k in d.keys():
        if d[k] is not None:
            out[k] = d[k]
    return out


def check_required_parameter(value, name: str):
    if not value and value != 0:
        raise ParameterRequiredError([name])


def check_required_parameters(params):
    """Validate multiple parameters
    params = [
        ['btcusdt', 'symbol'],
        [10, 'price']
    ]

    """
    for p in params:
        check_required_parameter(p[0], p[1])


def check_at_least_one_set_parameters(params):
    at_least_one_set = False
    for p in params:
        try:
            check_required_parameter(p[0], p[1])
            at_least_one_set = True
            break
        except:  # noqa: E722
            pass

    if not at_least_one_set:
        raise AtLeastOneParameterRequiredError()


def check_required_parameter_list(values: List, name: str):
    if len(values) == 0:
        raise ParameterRequiredError([name])

    for value in values:
        check_required_parameter(value, name)


def encode_string_list(L: List):
    return "[" + ",".join(f'"{i}"' for i in L) + "]"


def encoded_string(query):
    return urlencode(query, True).replace("%40", "@")


def convert_to_df(data, header: bool, index: str = None, apply_fn={}):
    df = pd.DataFrame(data)

    if header:
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header

    if index is not None:
        df = df.set_index(index)

    for idx, fn in apply_fn.items():
        if isinstance(idx, str):
            df[idx] = df[idx].apply(fn)
        else:
            df[df.columns[idx]] = df[df.columns[idx]].apply(fn)

    return df


def make_list(value):
    if not isinstance(value, list):
        value = [value]
    return value


def _postprocess(data, index):
    apply_fn = {}
    for idx in range(len(data[0]) - len(index)):
        apply_fn[idx] = to_float

    return convert_to_df(data, header=True, index=index, apply_fn=apply_fn)


def postprocess(num_index: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*arg, **kwarg):
            res = func(*arg, **kwarg)

            if not kwarg.get("pandas", True):
                return res

            if isinstance(res, dict):
                res["data"] = _postprocess(res["data"], res["data"][0][:num_index])
            else:
                res = _postprocess(res, res[0][:num_index])

            return res

        return wrapper

    return decorator
