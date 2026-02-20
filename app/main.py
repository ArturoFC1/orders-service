import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def cargar_pedidos():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("Error: orders.json no encontrado")
        return []
    except json.JSONDecodeError:
        print("Error: Formato JSON invalido")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def calcular_total_pedido(order: dict) -> float:
    total = 0.0

    for articulo in order["articulos"]:
        if not validar_articulo(articulo):
            print(f"Articulo invalido en la orden {order['id']}")
            continue
        subtotal = articulo["precio"] * articulo["cantidad"]
        total += subtotal

    return total


def filtrar_pedidos_caros(pedidos: list, min_total: float) -> list:
    filtro = []

    for order in pedidos:
        total = calcular_total_pedido(order)
        if total >= min_total:
            filtro.append(order)

    return filtro


def validar_articulo(item: dict) -> bool:
    match item:
        case {
            "precio": (int() | float()) as price,
            "cantidad": int(quantity),
        }:
            if price < 0 or quantity <= 0:
                return False
            return True
        case _:
            return False


def validar_nombre_cliente(nombre: str) -> bool:
    patron = r"^[A-Za-z\s]+$"
    return bool(re.match(patron, nombre))


def main():
    pedidos = cargar_pedidos()

    if not pedidos:
        print("No hay ordenes por procesar")
        return
    print(f"Cargados {len(pedidos)} pedidos")

    print("\nTodos los pedidos: ")
    for order in pedidos:
        total = calcular_total_pedido(order)
        order["orden_total"] = total
        print(f"Pedido {order['id']} - Cliente: {order['cliente']} - Total: ${total}")

    pedidos_caros = filtrar_pedidos_caros(pedidos, 10000)

    print("\nPedidos caros: ")
    for order in pedidos_caros:
        total = calcular_total_pedido(order)
        print(f"Pedido {order['id']} - Total: ${total}")

    for order in pedidos:
        if not validar_nombre_cliente(order["cliente"]):
            print(f"\nNombre del cliente invalido en la orden: {order['id']}\n")


if __name__ == "__main__":
    main()
