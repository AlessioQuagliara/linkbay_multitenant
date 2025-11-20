# schemas.py
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TenantStrategy(str, Enum):
    SCHEMA = "schema"
    DATABASE = "database"
    ROW = "row"


class TenantIdentificationMethod(str, Enum):
    HEADER = "header"
    SUBDOMAIN = "subdomain"
    COOKIE = "cookie"
    PATH_PARAM = "path_param"
    JWT_CLAIM = "jwt_claim"


class TenantContext(BaseModel):
    tenant_id: str
    schema_name: Optional[str] = None
    database_name: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True
