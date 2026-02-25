from pathlib import Path

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "http://localhost:8080"
REPORTS_PATH = Path(__file__).resolve().parent.parent.parent / "reports"


class OrderClient:
    def __init__(
        self, base_url: str = BASE_URL, timeout: float = 5.0, max_retries: int = 3
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def _get_with_retry(self, path: str) -> httpx.Response:
        for intento in range(1, self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(f"{self.base_url}{path}")
                    response.raise_for_status()
                    logger.info("GET %s - status %d", path, response.status_code)
                    return response
            except httpx.TimeoutException:
                logger.warning(
                    "Timeout en intento %d/%d para %s", intento, self.max_retries, path
                )
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error %d en %s", e.response.status_code, path)
                raise
            except httpx.RequestError as e:
                logger.warning(
                    "Error de conexion en intento %d/%d: %s",
                    intento,
                    self.max_retries,
                    e,
                )

            if intento == self.max_retries:
                raise ConnectionError(
                    f"Fallo despues de {self.max_retries} intentos: {path}"
                )

        raise ConnectionError(f"Fallo despues de {self.max_retries} intentos: {path}")

    def obtener_ordenes(self) -> list[dict]:
        response = self._get_with_retry("/orders")
        return response.json()

    def obtener_orden(self, order_id: int) -> dict:
        response = self._get_with_retry(f"/orders/{order_id}")
        return response.json()

    def descargar_reporte_streaming(self, filename: str = "report.csv") -> Path:
        REPORTS_PATH.mkdir(exist_ok=True)
        output_path = REPORTS_PATH / filename

        logger.info("Iniciando descarga streaming a %s", output_path)

        with httpx.Client(timeout=self.timeout) as client:
            with client.stream("GET", f"{self.base_url}/orders/report") as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=1024):
                        f.write(chunk)

        logger.info("Descarga completada: %s", output_path)
        return output_path
