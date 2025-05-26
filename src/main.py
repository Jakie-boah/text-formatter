from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.configs.logger import setup_logging

setup_logging()


app = FastAPI(
    title="NewsFeed-Formatter",
    docs_url="/docs",
    openapi_url="/api/openapi/",
    default_response_class=ORJSONResponse,
    root_path="/formatter-backend",
)


@app.get("/")
async def enter_point():
    return {"status": "Приложение запущено"}


logger.info("Starting FastAPI app")
