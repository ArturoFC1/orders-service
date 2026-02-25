import csv
from pathlib import Path

from app.models.item import Item
from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "orders.csv"


class CsvOrderLoader:
    @staticmethod
    def cargar_pedidos() -> list[Order]:
        try:
            pedidos: dict[int, Order] = {}

            with open(CSV_PATH, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order_id = int(row["id"])
                    item = Item(
                        nombre=row["nombre"],
                        precio=float(row["precio"]),
                        cantidad=int(row["cantidad"]),
                    )
                    if order_id not in pedidos:
                        pedidos[order_id] = Order(
                            id=order_id,
                            cliente=row["cliente"],
                            articulos=[],
                        )
                    pedidos[order_id].articulos.append(item)

            resultado = list(pedidos.values())
            logger.info("Se cargaron %d pedidos desde CSV", len(resultado))
            return resultado

        except FileNotFoundError:
            logger.error("orders.csv no encontrado en %s", CSV_PATH)
            return []
        except Exception as e:
            logger.exception("Error inesperado al cargar CSV: %s", e)
            return []
