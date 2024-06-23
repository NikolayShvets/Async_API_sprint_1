from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):  # type: ignore[no-redef]
    model_config = ConfigDict(from_attributes=True)
