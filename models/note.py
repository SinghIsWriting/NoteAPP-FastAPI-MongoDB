from pydantic import BaseModel
from datetime import datetime

class Note(BaseModel):
    id: int | None = None
    title: str | None = None
    note: str | None = None
    created_at: str | None = None
    important: bool = False
