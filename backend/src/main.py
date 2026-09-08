from fastapi import FastAPI

from interfaces.routers.artists import router as artists_router
from interfaces.routers.auth import router as auth_router
from interfaces.routers.events import router as events_router
from interfaces.routers.releases import router as releases_router

app = FastAPI()

app.include_router(artists_router)
app.include_router(releases_router)
app.include_router(events_router)
app.include_router(auth_router)