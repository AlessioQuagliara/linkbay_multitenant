#plugin.py
from dataclasses import dataclass
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .service import TenantServiceProtocol
from .schemas import TenantContext, TenantIdentificationMethod


@dataclass
class MultiTenantConfig:
    tenant_service: TenantServiceProtocol
    identification_method: TenantIdentificationMethod = TenantIdentificationMethod.HEADER
    header_name: str = "X-Tenant-ID"
    cookie_name: str = "tenant_id"
    subdomain_position: int = 0
    path_param_name: str = "tenant_id"
    jwt_claim_name: str = "tenant_id"
    require_tenant: bool = True


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: MultiTenantConfig):
        super().__init__(app)
        self.config = config

    async def dispatch(self, request: Request, call_next):
        tenant_id = self._identify_tenant(request)
        
        if tenant_id:
            tenant_context = await self.config.tenant_service.get_tenant_context(tenant_id)
            if tenant_context:
                request.state.tenant = tenant_context
                request.state.tenant_id = tenant_id
            elif self.config.require_tenant:
                raise HTTPException(status_code=404, detail=f"Tenant '{tenant_id}' not found")
        elif self.config.require_tenant:
            raise HTTPException(status_code=400, detail="Tenant not identified")
        
        return await call_next(request)

    def _identify_tenant(self, request: Request) -> Optional[str]:
        method = self.config.identification_method
        
        if method == TenantIdentificationMethod.HEADER:
            return request.headers.get(self.config.header_name)
        
        elif method == TenantIdentificationMethod.SUBDOMAIN:
            host = request.headers.get("host", "")
            parts = host.split(".")
            if len(parts) > 2:
                return parts[self.config.subdomain_position]
        
        elif method == TenantIdentificationMethod.COOKIE:
            return request.cookies.get(self.config.cookie_name)
        
        elif method == TenantIdentificationMethod.PATH_PARAM:
            return request.path_params.get(self.config.path_param_name)
        
        elif method == TenantIdentificationMethod.JWT_CLAIM:
            # Cerca il claim JWT nello state (deve essere settato da un middleware auth precedente)
            if hasattr(request.state, "jwt_payload"):
                return request.state.jwt_payload.get(self.config.jwt_claim_name)
        
        return None


class LinkBayMultiTenantPlugin:
    def __init__(self, config: MultiTenantConfig):
        self.config = config

    def install(self, app: FastAPI):
        app.add_middleware(TenantMiddleware, config=self.config)
