from pydantic import BaseModel

class BaseSchema(BaseModel):
    id: int | None = None
