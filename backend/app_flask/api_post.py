from functools import wraps
from typing import Any, Callable, Literal, Type, cast

from apiflask import APIBlueprint
from pydantic import BaseModel


def api_route(
    bp: APIBlueprint,
    url: str,
    method: Literal["get", "post"] = "post",
    input_model: Type[BaseModel] | None = None,
    output_model: Type[BaseModel] | None = None,
    arg_name: str = "data",
):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if arg_name in kwargs:
                data = kwargs.pop(arg_name)
                return func(data, *args, **kwargs)

            return func(*args, **kwargs)

        route_func = wrapper

        if input_model is not None:
            route_func = bp.input(
                cast(Any, input_model),
                arg_name=arg_name,
            )(route_func)

        if output_model is not None:
            route_func = bp.output(cast(Any, output_model))(route_func)

        return getattr(bp, method)(url)(route_func)

    return decorator
