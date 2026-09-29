from fastapi import FastAPI

from magnify_api.interfaces.routers import router as events_router
from magnify_api.interfaces.routers.artists import router as artists_router
from magnify_api.interfaces.routers.auth import router as auth_router
from magnify_api.interfaces.routers.me import router as me_router
from magnify_api.interfaces.routers.releases import router as releases_router
from magnify_api.interfaces.routers.users import router as users_router

app = FastAPI()

app.include_router(artists_router)
app.include_router(releases_router)
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(me_router)