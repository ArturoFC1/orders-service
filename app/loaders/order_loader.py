import json
from pathlib import Path

from app.models.item import Item
from app.models.order import Order

# Esta clase carga datos del JSON

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "orders.json"


class OrderLoader:
    @staticmethod
    def cargar_pedidos() -> list[Order]:
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [
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

        except FileNotFoundError:
            print("Error: orders.json no encontrado")
            return []
        except json.JSONDecodeError:
            print("Error: Formato JSON invalido")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
