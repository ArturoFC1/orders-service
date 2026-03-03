from app.application.dtos.order_dtos import CreateOrderDTO, ItemDTO, OrderResponseDTO
from app.domain.entities.item import Item
from app.domain.entities.order import Order
from app.domain.ports.notification_port import NotificationPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepositoryPort,
        notification: NotificationPort,
    ) -> None:
        self.repository = repository
        self.notification = notification

    def execute(self, dto: CreateOrderDTO) -> OrderResponseDTO:
        articulos = [
            Item(nombre=i.nombre, precio=i.precio, cantidad=i.cantidad)
            for i in dto.items
        ]
        order = Order(id=0, cliente=dto.cliente, articulos=articulos)
        saved = self.repository.guardar(order)
        self.notification.notificar_orden_creada(saved)
        logger.info("Orden creada: id=%d cliente=%s", saved.id, saved.cliente)
        return OrderResponseDTO(
            id=saved.id,
            cliente=saved.cliente,
            total=saved.calcular_total(),
            items=[
                ItemDTO(nombre=i.nombre, precio=i.precio, cantidad=i.cantidad)
                for i in saved.articulos
            ],
        )


class GetOrderUseCase:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self.repository = repository

    def execute(self, order_id: int) -> OrderResponseDTO | None:
        order = self.repository.obtener_por_id(order_id)
        if not order:
            logger.warning("Orden %d no encontrada", order_id)
            return None
        return OrderResponseDTO(
            id=order.id,
            cliente=order.cliente,
            total=order.calcular_total(),
            items=[
                ItemDTO(nombre=i.nombre, precio=i.precio, cantidad=i.cantidad)
                for i in order.articulos
            ],
        )


class DeleteOrderUseCase:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self.repository = repository

    def execute(self, order_id: int) -> bool:
        result = self.repository.eliminar(order_id)
        if result:
            logger.info("Orden %d eliminada", order_id)
        return result


class ListOrdersUseCase:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self.repository = repository

    def execute(self) -> list[OrderResponseDTO]:
        orders = self.repository.obtener_todos()
        return [
            OrderResponseDTO(
                id=o.id,
                cliente=o.cliente,
                total=o.calcular_total(),
                items=[
                    ItemDTO(nombre=i.nombre, precio=i.precio, cantidad=i.cantidad)
                    for i in o.articulos
                ],
            )
            for o in orders
        ]
