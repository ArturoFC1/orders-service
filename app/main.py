import random
import time
from contextlib import contextmanager

from app.loaders.order_loader import OrderLoader
from app.models.order_schemas import OrderIn
from app.services.order_service import OrderService
from app.utils.order_mapper import entity_to_order_out, order_in_to_entity
from app.utils.retry import retry


def generador_por_lotes(elementos, tamaño_lote):
    for i in range(0, len(elementos), tamaño_lote):
        yield elementos[i : i + tamaño_lote]


@contextmanager
def timer(name):
    start = time.time()
    print(f"Iniciando {name}...")
    yield
    print(f"{name} tardó {time.time() - start:.4f} segundos")


@retry
def operacion_inestable():
    if random.random() < 0.7:
        raise ValueError("El servidor no respondio")
    return "Conexion exitosa"


def demo_pydantic():
    raw = {
        "id": 99,
        "cliente": "Test User",
        "articulos": [{"nombre": "Teclado", "precio": 500, "cantidad": 2}],
    }
    order_in = OrderIn(**raw)
    order = order_in_to_entity(order_in)
    order_out = entity_to_order_out(order)
    print("\nDemo Pydantic:")
    print(order_out.model_dump())


def main():
    print(operacion_inestable())

    pedidos = OrderLoader.cargar_pedidos()

    if not pedidos:
        print("No hay ordenes por procesar")
        return
    print(f"Cargados {len(pedidos)} pedidos")

    service = OrderService(pedidos)

    print("\nTodos los pedidos:")
    for order in pedidos:
        order.orden_total = service.calcular_total(order)
        print(
            f"Pedido {order.id} - Cliente: {order.cliente} - Total: ${order.orden_total}"
        )

    print("\nPedidos caros:")
    for order in service.filtrar_pedidos_caros(10000):
        print(f"Pedido {order.id} - Total: ${service.calcular_total(order)}")

    service.validar_clientes()

    for batch in generador_por_lotes(pedidos, 2):
        print("Lote:")
        for order in batch:
            print(f"Orden: {order.id}")

    with timer("Procesamiento"):
        operacion_inestable()

    demo_pydantic()


if __name__ == "__main__":
    main()
