from pydantic import BaseModel
from pydantic import ConfigDict


class BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
