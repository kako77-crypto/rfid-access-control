from pydantic import BaseModel, Field


class AccessCheckRequest(BaseModel):
    reader_code: str = Field(min_length=1, max_length=64)
    uid: str = Field(min_length=1, max_length=64)


class AccessCheckResponse(BaseModel):
    authorized: bool
    reason: str
    uid: str
    user_id: int | None = None
    user_name: str | None = None
