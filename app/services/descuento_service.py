from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)

DESCUENTO_MINIMO_TOTAL = 10000
PORCENTAJE_DESCUENTO = 0.10


class DescuentoService:
    def aplicar_descuento(self, order: Order) -> float:
        total = order.calcular_total()

        if total > DESCUENTO_MINIMO_TOTAL:
            total_con_descuento = total * (1 - PORCENTAJE_DESCUENTO)
            logger.debug(
                "Descuento aplicado a orden %d: $%.2f -> $%.2f",
                order.id,
                total,
                total_con_descuento,
            )
            return max(0.0, total_con_descuento)

        return total
