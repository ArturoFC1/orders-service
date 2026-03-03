from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.order_dtos import CreateOrderDTO, OrderResponseDTO
from app.application.use_cases.order_use_cases import (
    CreateOrderUseCase,
    DeleteOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
)
from app.infrastructure.api.dependencies import get_current_user, get_db
from app.infrastructure.database.models import User
from app.infrastructure.notifications.http_notification_adapter import (
    LogNotificationAdapter,
)
from app.infrastructure.repositories.sql_order_repository import SqlOrderRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_use_cases(
    db: Session = Depends(get_db),
) -> tuple:
    repo = SqlOrderRepository(db)
    notification = LogNotificationAdapter()
    return (
        CreateOrderUseCase(repo, notification),
        GetOrderUseCase(repo),
        DeleteOrderUseCase(repo),
        ListOrdersUseCase(repo),
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponseDTO)
def crear_order(
    order_data: CreateOrderDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SqlOrderRepository(db)
    notification = LogNotificationAdapter()
    use_case = CreateOrderUseCase(repo, notification)
    return use_case.execute(order_data)


@router.get("/", response_model=list[OrderResponseDTO])
def listar_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = ListOrdersUseCase(SqlOrderRepository(db))
    return use_case.execute()


@router.get("/{order_id}", response_model=OrderResponseDTO)
def obtener_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = GetOrderUseCase(SqlOrderRepository(db))
    order = use_case.execute(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteOrderUseCase(SqlOrderRepository(db))
    if not use_case.execute(order_id):
        raise HTTPException(status_code=404, detail="Orden no encontrada")
