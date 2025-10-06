from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: int
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: str
    last_activity: str

@dataclass
class Admin:
    id: int
    user_id: int
    username: Optional[str]
    permissions: str
    created_at: str
    created_by: int