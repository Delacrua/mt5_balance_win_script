from datetime import datetime

from pydantic import BaseModel


__all__ = [
    "AccountInfoResponse",
]


class AccountInfoResponse(BaseModel):
    login: int
    balance: float
    equity: float
    created_at: datetime = datetime.utcnow()
