from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id: int = 1

    def obtener_todos(self) -> list[Order]:
        return list(self._orders.values())

    def obtener_por_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def guardar(self, order: Order) -> Order:
        if order.id == 0:
            order.id = self._next_id
            self._next_id += 1
        self._orders[order.id] = order
        logger.debug("Orden guardada en memoria: %d", order.id)
        return order

    def eliminar(self, order_id: int) -> bool:
        if order_id in self._orders:
            del self._orders[order_id]
            logger.debug("Orden eliminada de memoria: %d", order_id)
            return True
        return False
