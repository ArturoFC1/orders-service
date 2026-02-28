from app.models.order import Order
from app.ports.order_repository import OrderRepositoryPort
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CachedOrderRepository:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self._repository = repository
        self._cache: dict[int, Order] = {}

    def obtener_todos(self) -> list[Order]:
        orders = self._repository.obtener_todos()
        for order in orders:
            self._cache[order.id] = order
        logger.debug("Cache actualizado con %d ordenes", len(orders))
        return orders

    def obtener_por_id(self, order_id: int) -> Order | None:
        if order_id in self._cache:
            logger.debug("Cache hit para orden %d", order_id)
            return self._cache[order_id]
        order = self._repository.obtener_por_id(order_id)
        if order:
            self._cache[order_id] = order
            logger.debug("Cache miss para orden %d, guardado en cache", order_id)
        return order

    def guardar(self, order: Order) -> Order:
        saved = self._repository.guardar(order)
        self._cache[saved.id] = saved
        logger.debug("Orden %d guardada y cacheada", saved.id)
        return saved

    def eliminar(self, order_id: int) -> bool:
        result = self._repository.eliminar(order_id)
        if result and order_id in self._cache:
            del self._cache[order_id]
            logger.debug("Orden %d eliminada del cache", order_id)
        return result
