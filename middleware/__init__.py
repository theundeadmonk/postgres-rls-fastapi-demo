from contextvars import ContextVar

from starlette.datastructures import Headers
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.types import ASGIApp
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send


global_tenant_id: ContextVar[str] = ContextVar("global_tenant_id", default=None)


class PostgresRLSMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in (
            "http",
            "websocket",
        ):
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_tenant_id = headers.get("X-Tenant-Id")

        response: Response
        if request_tenant_id is None:
            response = JSONResponse(
                {
                    "error": "Tenant must be provided",
                },
                status_code=401,
                headers=dict(headers),
            )
            await response(scope, receive, send)
        else:
            global_tenant_id.set(request_tenant_id)
            await self.app(scope, receive, send)