import json
from pathlib import Path

from app.models.item import Item
from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "orders.json"


class OrderLoader:
    @staticmethod
    def cargar_pedidos() -> list[Order]:
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            pedidos = [
                Order(
                    id=item["id"],
                    cliente=item["cliente"],
                    articulos=[
                        Item(
                            nombre=a["nombre"],
                            precio=a["precio"],
                            cantidad=a["cantidad"],
                        )
                        for a in item["articulos"]
                    ],
                )
                for item in data
            ]
            logger.info("Se cargaron %d pedidos desde JSON", len(pedidos))
            return pedidos

        except FileNotFoundError:
            logger.error("orders.json no encontrado en %s", DATA_PATH)
            return []
        except json.JSONDecodeError:
            logger.error("Formato JSON invalido en %s", DATA_PATH)
            return []
        except Exception as e:
            logger.exception("Error inesperado al cargar pedidos: %s", e)
            return []
