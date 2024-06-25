from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel


class GenericAPIError(BaseModel):
    code: int
    message: str


class GenericAPIResponse(BaseModel):
    success: bool
    response: dict[str, Any]
    status_code: int
    errors: Optional[GenericAPIError]


class TimeMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
