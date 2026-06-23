from pydantic import BaseModel



def send_message(model: BaseModel | None = None) -> BaseModel | dict:

    if model:
        return model
    else:
        return {"status": "ok"}
