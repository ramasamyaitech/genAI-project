from fastapi import FastAPI

from api import router

from config import settings

app = FastAPI(

    title=settings.APP_NAME,

    version="1.0.0"
)

app.include_router(router)