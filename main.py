from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.routes import router
from src.application.job_service import JobService
from src.application.report_service import ReportService
from src.infrastructure.clients.dummyjson_client import DummyJsonClient
from src.infrastructure.clients.legacy_client import get_user_todos_sync
from src.infrastructure.job_store import JobStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    dummyjson_client = DummyJsonClient()
    app.state.dummyjson_client = dummyjson_client
    app.state.job_store = JobStore()
    app.state.report_service = ReportService(
        user_client=dummyjson_client,
        todos_client=get_user_todos_sync
    )
    app.state.job_service = JobService(
        report_service=app.state.report_service,
        job_store=app.state.job_store
    )
    yield
    await dummyjson_client.aclose()


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "displayRequestDuration": True,
    },
)
app.include_router(router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )