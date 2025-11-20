#dependencies.py
from fastapi import Request, Depends, HTTPException
from .schemas import TenantContext


async def get_tenant_context(request: Request) -> TenantContext:
    """Dependency per ottenere il contesto tenant."""
    if not hasattr(request.state, "tenant"):
        raise HTTPException(status_code=400, detail="Tenant context not available")
    return request.state.tenant


async def get_tenant_id(request: Request) -> str:
    """Dependency per ottenere il tenant_id."""
    if not hasattr(request.state, "tenant_id"):
        raise HTTPException(status_code=400, detail="Tenant ID not available")
    return request.state.tenant_id
