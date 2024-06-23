from pydantic import BaseModel, ConfigDict


class BaseModel(BaseModel):  # type: ignore[no-redef]
    model_config = ConfigDict(from_attributes=True)
