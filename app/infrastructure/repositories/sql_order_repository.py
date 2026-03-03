from sqlalchemy.orm import Session

from app.domain.entities.item import Item
from app.domain.entities.order import Order
from app.infrastructure.database.models import OrderItemModel, OrderModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SqlOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def obtener_todos(self) -> list[Order]:
        order_models = self.session.query(OrderModel).all()
        return [self._to_domain(om) for om in order_models]

    def obtener_por_id(self, order_id: int) -> Order | None:
        om = self.session.get(OrderModel, order_id)
        return self._to_domain(om) if om else None

    def guardar(self, order: Order) -> Order:
        om = OrderModel(user_id=order.id)
        self.session.add(om)
        self.session.flush()
        for item in order.articulos:
            oi = OrderItemModel(
                order_id=om.id,
                nombre=item.nombre,
                precio=item.precio,
                cantidad=item.cantidad,
            )
            self.session.add(oi)
        self.session.commit()
        order.id = om.id
        logger.debug("Orden guardada en SQL: %d", order.id)
        return order

    def eliminar(self, order_id: int) -> bool:
        om = self.session.get(OrderModel, order_id)
        if not om:
            return False
        self.session.delete(om)
        self.session.commit()
        logger.debug("Orden eliminada de SQL: %d", order_id)
        return True

    def _to_domain(self, om: OrderModel) -> Order:
        articulos = [
            Item(nombre=i.nombre, precio=i.precio, cantidad=i.cantidad)
            for i in om.items
        ]
        cliente = om.user.nombre if om.user else f"User_{om.user_id}"
        return Order(id=om.id, cliente=cliente, articulos=articulos)
