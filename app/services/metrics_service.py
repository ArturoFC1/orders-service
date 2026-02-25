import json
from pathlib import Path

from app.models.order import Order
from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
REPORTS_PATH = BASE_DIR / "reports"


class MetricsService:
    def __init__(self, pedidos: list[Order]):
        self.pedidos = pedidos

    def calcular_metricas(self) -> dict:
        totales = [order.calcular_total() for order in self.pedidos]

        if not totales:
            logger.warning("No hay pedidos para calcular metricas")
            return {}

        pedido_mas_caro = max(self.pedidos, key=lambda o: o.calcular_total())

        metricas = {
            "total_pedidos": len(self.pedidos),
            "total_vendido": sum(totales),
            "promedio_por_pedido": sum(totales) / len(totales),
            "pedido_mas_caro": {
                "id": pedido_mas_caro.id,
                "cliente": pedido_mas_caro.cliente,
                "total": pedido_mas_caro.calcular_total(),
            },
            "por_cliente": {
                order.cliente: order.calcular_total() for order in self.pedidos
            },
        }

        logger.debug("Metricas calculadas: %s", metricas)
        return metricas

    def exportar_json(self, filename: str = "metrics.json") -> None:
        REPORTS_PATH.mkdir(exist_ok=True)
        metricas = self.calcular_metricas()

        if not metricas:
            return

        output_path = REPORTS_PATH / filename
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(metricas, file, indent=2, ensure_ascii=False)

        logger.info("Metricas exportadas a %s", output_path)
