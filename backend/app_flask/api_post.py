from typing import Type, cast, Any, Literal
from apiflask import APIBlueprint
from pydantic import BaseModel


def api_route(
    bp: APIBlueprint,
    url: str,
    method: Literal["get", "post"] = "post",
    input_model: Type[BaseModel] | None = None,
    output_model: Type[BaseModel] | None = None,
):
    def decorator(func):
        f = func

        if input_model:
            f = bp.input(cast(Any, input_model))(f)

        if output_model:
            f = bp.output(cast(Any, output_model))(f)

        f = getattr(bp, method)(url)(f)  # 🔥 без if

        return f

    return decorator
