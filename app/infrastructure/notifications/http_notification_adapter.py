import httpx

from app.domain.entities.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)

NOTIFICATION_URL = "http://localhost:8080/notifications"


class HttpNotificationAdapter:
    def __init__(self, url: str = NOTIFICATION_URL, timeout: float = 3.0) -> None:
        self.url = url
        self.timeout = timeout

    def notificar_orden_creada(self, order: Order) -> None:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                client.post(
                    self.url,
                    json={
                        "event": "order_created",
                        "order_id": order.id,
                        "cliente": order.cliente,
                        "total": order.calcular_total(),
                    },
                )
            logger.info("Notificacion enviada para orden %d", order.id)
        except Exception as e:
            logger.warning("Fallo notificacion para orden %d: %s", order.id, e)


class LogNotificationAdapter:
    """Adaptador simple que solo loguea, util para tests y desarrollo."""

    def notificar_orden_creada(self, order: Order) -> None:
        logger.info(
            "Orden creada notificada: id=%d cliente=%s total=%.2f",
            order.id,
            order.cliente,
            order.calcular_total(),
        )
