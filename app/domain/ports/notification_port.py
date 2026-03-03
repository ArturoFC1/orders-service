from typing import Protocol, runtime_checkable

from app.domain.entities.order import Order


@runtime_checkable
class NotificationPort(Protocol):
    def notificar_orden_creada(self, order: Order) -> None: ...
