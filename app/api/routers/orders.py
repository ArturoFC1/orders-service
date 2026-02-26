from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.database.crud import (
    crear_orden,
    eliminar_orden,
    obtener_orden,
    obtener_ordenes_por_usuario,
)
from app.database.models import User
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


class ItemIn(BaseModel):
    nombre: str
    precio: float
    cantidad: int


class OrderCreate(BaseModel):
    items: list[ItemIn]


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = [item.model_dump() for item in order_data.items]
    order = crear_orden(db, current_user.id, items)
    logger.info("Orden creada por usuario %s", current_user.email)
    return {"id": order.id, "user_id": order.user_id, "total": order.total()}


@router.get("/")
def listar_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = obtener_ordenes_por_usuario(db, current_user.id)
    return [{"id": o.id, "total": o.total()} for o in orders]


@router.get("/{order_id}")
def obtener_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = obtener_orden(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"id": order.id, "user_id": order.user_id, "total": order.total()}


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = obtener_orden(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    eliminar_orden(db, order_id)
    logger.info("Orden %d eliminada por usuario %s", order_id, current_user.email)
