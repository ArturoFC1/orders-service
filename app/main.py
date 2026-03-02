import asyncio
import random
import time
from contextlib import contextmanager

from app.clients.order_client import OrderClient
from app.database.crud import (
    crear_orden,
    crear_usuario,
    eliminar_orden,
    obtener_ordenes_por_usuario,
    obtener_todos_usuarios,
)
from app.database.engine import SessionLocal
from app.database.models import OrderItemModel, OrderModel, User
from app.loaders.csv_order_loader import CsvOrderLoader
from app.loaders.order_loader import OrderLoader
from app.ml.order_classifier import entrenar_modelo, predecir
from app.models.order_schemas import OrderIn
from app.services.concurrencia_service import (
    calcular_primos_paralelo,
    calcular_primos_secuencial,
    fetch_all_async,
    fetch_all_sync,
)
from app.services.metrics_service import MetricsService
from app.services.order_service import OrderService
from app.utils.logger import get_logger
from app.utils.order_mapper import entity_to_order_out, order_in_to_entity
from app.utils.retry import retry

logger = get_logger(__name__)


def generador_por_lotes(elementos, tamaño_lote):
    for i in range(0, len(elementos), tamaño_lote):
        yield elementos[i : i + tamaño_lote]


@contextmanager
def timer(name):
    start = time.time()
    logger.info("Iniciando %s...", name)
    yield
    logger.info("%s tardó %.4f segundos", name, time.time() - start)


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
    logger.debug("Demo Pydantic: %s", order_out.model_dump())


def demo_csv_metricas():
    logger.info("--- Demo CSV y Metricas ---")
    pedidos_csv = CsvOrderLoader.cargar_pedidos()

    if not pedidos_csv:
        logger.warning("No se pudieron cargar pedidos del CSV")
        return

    metrics = MetricsService(pedidos_csv)
    metrics.exportar_json()


def demo_http_client():
    logger.info("--- Demo HTTP Client ---")
    client = OrderClient()

    ordenes = client.obtener_ordenes()
    logger.info("Ordenes obtenidas: %s", ordenes)

    orden = client.obtener_orden(1)
    logger.info("Orden 1: %s", orden)

    path = client.descargar_reporte_streaming()
    logger.info("Reporte descargado en: %s", path)


def demo_database():
    logger.info("--- Demo Database ---")
    session = SessionLocal()

    try:
        session.query(OrderItemModel).delete()
        session.query(OrderModel).delete()
        session.query(User).delete()
        session.commit()

        user1 = crear_usuario(session, "Juan Perez", "juan@example.com")
        user2 = crear_usuario(session, "Maria Lopez", "maria@example.com")

        crear_orden(
            session,
            user1.id,
            [
                {"nombre": "Laptop", "precio": 15000, "cantidad": 1},
                {"nombre": "Mouse", "precio": 300, "cantidad": 2},
            ],
        )

        crear_orden(
            session,
            user2.id,
            [
                {"nombre": "Monitor", "precio": 4000, "cantidad": 2},
            ],
        )

        usuarios = obtener_todos_usuarios(session)
        for user in usuarios:
            ordenes = obtener_ordenes_por_usuario(session, user.id)
            for order in ordenes:
                logger.info(
                    "User: %s | Orden %d | Total: $%.2f",
                    user.nombre,
                    order.id,
                    order.total(),
                )

        eliminar_orden(session, 1)

    finally:
        session.close()


def demo_concurrencia():
    logger.info("--- Demo Concurrencia ---")

    order_ids = [1, 2, 3, 4, 5]

    logger.info("Fetch sincrono:")
    fetch_all_sync(order_ids)

    logger.info("Fetch asincrono:")
    asyncio.run(fetch_all_async(order_ids))

    limites = [500_000, 1_000_000, 2_000_000, 500_000]

    logger.info("Calculo de primos secuencial:")
    calcular_primos_secuencial(limites)

    logger.info("Calculo de primos paralelo:")
    calcular_primos_paralelo(limites)


def demo_ml():
    logger.info("--- Demo Machine Learning ---")
    entrenar_modelo()

    casos = [
        {"total": 15000, "num_items": 1, "precio_promedio": 15000},
        {"total": 500, "num_items": 2, "precio_promedio": 250},
        {"total": 12000, "num_items": 3, "precio_promedio": 4000},
    ]

    for caso in casos:
        resultado = predecir(**caso)
        logger.info(
            "Total: $%d | Es cara: %s | Prob: %.2f%%",
            caso["total"],
            resultado["es_cara"],
            resultado["probabilidad_cara"] * 100,
        )


def main():
    logger.info(operacion_inestable())

    pedidos = OrderLoader.cargar_pedidos()

    if not pedidos:
        logger.warning("No hay ordenes por procesar")
        return

    service = OrderService(pedidos)

    logger.info("Todos los pedidos:")
    for order in pedidos:
        order.orden_total = service.calcular_total(order)
        logger.info(
            "Pedido %s - Cliente: %s - Total: $%.2f",
            order.id,
            order.cliente,
            order.orden_total,
        )

    logger.info("Pedidos caros:")
    for order in service.filtrar_pedidos_caros(10000):
        logger.info("Pedido %s - Total: $%.2f", order.id, service.calcular_total(order))

    service.validar_clientes()

    for batch in generador_por_lotes(pedidos, 2):
        logger.debug("Lote: %s", [order.id for order in batch])

    with timer("Procesamiento"):
        operacion_inestable()

    demo_pydantic()

    demo_csv_metricas()

    demo_http_client()

    demo_database()

    demo_concurrencia()

    demo_ml()


if __name__ == "__main__":
    main()
