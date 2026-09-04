from fastapi import FastAPI

from interfaces.routers.artists import router as artists_router

app = FastAPI()

app.include_router(artists_router)