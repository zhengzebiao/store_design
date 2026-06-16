from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import assets, components, pages, templates
from app.core.config import settings
from app.core.errors import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(templates.router, prefix="/api/store-design", tags=["templates"])
    app.include_router(pages.router, prefix="/api/store-design", tags=["pages"])
    app.include_router(components.router, prefix="/api/store-design", tags=["components"])
    app.include_router(assets.router, prefix="/api/store-design", tags=["assets"])
    return app


app = create_app()
