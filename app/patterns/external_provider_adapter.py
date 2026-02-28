from app.models.item import Item
from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExternalProviderOrder:
    """Simula el formato de datos de un proveedor externo."""

    def __init__(self, data: dict) -> None:
        self.order_number = data["order_number"]
        self.customer_name = data["customer_name"]
        self.line_items = data["line_items"]


class ExternalProviderAdapter:
    """Adapta el formato externo al dominio interno."""

    def to_domain(self, external: ExternalProviderOrder) -> Order:
        articulos = [
            Item(
                nombre=li["product_name"],
                precio=float(li["unit_price"]),
                cantidad=int(li["qty"]),
            )
            for li in external.line_items
        ]
        order = Order(
            id=int(external.order_number.replace("EXT-", "")),
            cliente=external.customer_name,
            articulos=articulos,
        )
        logger.debug("Orden externa %s adaptada al dominio", external.order_number)
        return order
