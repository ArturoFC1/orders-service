import asyncio
import math
import time
from concurrent.futures import ProcessPoolExecutor

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "http://localhost:8080"


# --- Version sincrona ---
def fetch_order_sync(order_id: int) -> dict:
    with httpx.Client(timeout=5.0) as client:
        response = client.get(f"{BASE_URL}/orders/{order_id}")
        response.raise_for_status()
        return response.json()


def fetch_all_sync(order_ids: list[int]) -> list[dict]:
    start = time.time()
    results = [fetch_order_sync(oid) for oid in order_ids]
    elapsed = time.time() - start
    logger.info("Sincrono: %d ordenes en %.4f segundos", len(results), elapsed)
    return results


# --- Version asincrona con semaforo ---
async def fetch_order_async(
    client: httpx.AsyncClient, order_id: int, semaforo: asyncio.Semaphore
) -> dict:
    async with semaforo:
        response = await client.get(f"{BASE_URL}/orders/{order_id}")
        response.raise_for_status()
        logger.debug("Orden %d obtenida async", order_id)
        return response.json()


async def fetch_all_async(order_ids: list[int], max_concurrent: int = 3) -> list[dict]:
    semaforo = asyncio.Semaphore(max_concurrent)
    start = time.time()

    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [fetch_order_async(client, oid, semaforo) for oid in order_ids]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    logger.info("Asincrono: %d ordenes en %.4f segundos", len(results), elapsed)
    return list(results)


# --- CPU-bound con ProcessPoolExecutor ---
def calcular_primos(n: int) -> int:
    """Cuenta cuántos primos hay hasta n usando criba de Eratóstenes."""
    if n < 2:
        return 0
    criba = [True] * (n + 1)
    criba[0] = criba[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if criba[i]:
            for j in range(i * i, n + 1, i):
                criba[j] = False
    return sum(criba)


def calcular_primos_paralelo(limites: list[int]) -> list[int]:
    start = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(calcular_primos, limites))
    elapsed = time.time() - start
    logger.info(
        "ProcessPoolExecutor: %d calculos en %.4f segundos", len(limites), elapsed
    )
    return results


def calcular_primos_secuencial(limites: list[int]) -> list[int]:
    start = time.time()
    results = [calcular_primos(n) for n in limites]
    elapsed = time.time() - start
    logger.info("Secuencial: %d calculos en %.4f segundos", len(limites), elapsed)
    return results
