from typing import Protocol

from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PricingStrategy(Protocol):
    def calcular(self, order: Order) -> float: ...


class PrecioNormal:
    def calcular(self, order: Order) -> float:
        total = order.calcular_total()
        logger.debug("Precio normal aplicado: $%.2f", total)
        return total


class DescuentoVolumen:
    def __init__(self, min_items: int = 5, descuento: float = 0.15) -> None:
        self.min_items = min_items
        self.descuento = descuento

    def calcular(self, order: Order) -> float:
        total_items = sum(item.cantidad for item in order.articulos)
        total = order.calcular_total()
        if total_items >= self.min_items:
            total = total * (1 - self.descuento)
            logger.debug("Descuento volumen aplicado: $%.2f", total)
        return total


class PrecioVIP:
    def __init__(self, descuento: float = 0.20) -> None:
        self.descuento = descuento

    def calcular(self, order: Order) -> float:
        total = order.calcular_total() * (1 - self.descuento)
        logger.debug("Precio VIP aplicado: $%.2f", total)
        return total


class PricingService:
    def __init__(self, strategy: PricingStrategy) -> None:
        self.strategy = strategy

    def calcular_precio(self, order: Order) -> float:
        return self.strategy.calcular(order)

    def cambiar_estrategia(self, strategy: PricingStrategy) -> None:
        self.strategy = strategy
        logger.debug("Estrategia cambiada a %s", strategy.__class__.__name__)
