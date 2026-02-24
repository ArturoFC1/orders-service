from dataclasses import dataclass, field

from app.models.item import Item


@dataclass
class Order:
    id: int
    cliente: str
    articulos: list[Item] = field(default_factory=list)
    orden_total: float = 0.0

    def calcular_total(self) -> float:
        return sum(item.subtotal() for item in self.articulos if item.es_valido())

    def es_valido(self) -> bool:
        return isinstance(self.cliente, str) and len(self.cliente) > 0

    def __lt__(self, other: "Order") -> bool:
        return self.calcular_total() < other.calcular_total()

    def __eq__(self, other: "Order") -> bool:
        return self.calcular_total() == other.calcular_total()
