#service.py
from typing import Protocol, Optional, Callable, Awaitable
from fastapi import Request
from .schemas import TenantContext


class TenantServiceProtocol(Protocol):
    """Protocol che l'app madre deve implementare per gestire i tenant."""
    
    async def get_tenant_context(self, tenant_id: str) -> Optional[TenantContext]:
        """Recupera il contesto del tenant dal database."""
        ...
