from app.models.order import Order
from app.ports.order_repository import OrderRepositoryPort
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OrderDomainService:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self.repository = repository

    def obtener_todas(self) -> list[Order]:
        return self.repository.obtener_todos()

    def obtener_por_id(self, order_id: int) -> Order | None:
        order = self.repository.obtener_por_id(order_id)
        if not order:
            logger.warning("Orden %d no encontrada", order_id)
        return order

    def guardar(self, order: Order) -> Order:
        return self.repository.guardar(order)

    def eliminar(self, order_id: int) -> bool:
        return self.repository.eliminar(order_id)

    def total_vendido(self) -> float:
        return sum(o.calcular_total() for o in self.repository.obtener_todos())
