from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, orders
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Orders Service API",
    description="API para gestión de órdenes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(orders.router)


@app.get("/health")
def health():
    return {"status": "ok"}
