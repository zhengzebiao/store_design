from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.response import failure


class BusinessError(Exception):
    def __init__(self, error_code: str, error_info: str, status_code: int = 400, details: dict | None = None) -> None:
        self.error_code = error_code
        self.error_info = error_info
        self.status_code = status_code
        self.details = details or {}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(BusinessError)
    async def handle_business_error(_: Request, exc: BusinessError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=failure(exc.error_code, exc.error_info, exc.details),
        )
