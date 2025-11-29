from fastapi import FastAPI
from .accounts import router as acc_router
from .telegram import router as tg_router
from .users import router as us_router

def include_routers(app: FastAPI):
    app.include_router(tg_router)
    app.include_router(acc_router)
    app.include_router(us_router)