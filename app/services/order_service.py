from app.models.order import Order
from app.models.type_definitions import Calculable
from app.utils.logger import get_logger
from app.utils.validators import validar_nombre_cliente

logger = get_logger(__name__)


class OrderService:
    def __init__(self, pedidos: list[Order]):
        self.pedidos = pedidos

    def calcular_total(self, order: Calculable) -> float:
        total = 0.0
        for articulo in order.articulos:
            if not articulo.es_valido():
                logger.warning("Articulo invalido en la orden %s", order.id)
                continue
            total += articulo.subtotal()
        return total

    def filtrar_pedidos_caros(self, min_total: float) -> list[Order]:
        resultado = [
            order for order in self.pedidos if self.calcular_total(order) >= min_total
        ]
        logger.debug(
            "Pedidos filtrados con min_total=%.2f: %d encontrados",
            min_total,
            len(resultado),
        )
        return resultado

    def validar_clientes(self) -> None:
        for order in self.pedidos:
            if not validar_nombre_cliente(order.cliente):
                logger.warning("Nombre del cliente invalido en la orden: %s", order.id)
