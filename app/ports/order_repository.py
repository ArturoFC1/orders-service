from typing import Protocol, runtime_checkable

from app.models.order import Order


@runtime_checkable
class OrderRepositoryPort(Protocol):
    def obtener_todos(self) -> list[Order]: ...

    def obtener_por_id(self, order_id: int) -> Order | None: ...

    def guardar(self, order: Order) -> Order: ...

    def eliminar(self, order_id: int) -> bool: ...
