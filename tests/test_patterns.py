from app.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)
from app.models.item import Item
from app.models.order import Order
from app.patterns.cached_repository import CachedOrderRepository
from app.patterns.external_provider_adapter import (
    ExternalProviderAdapter,
    ExternalProviderOrder,
)
from app.patterns.pricing_strategy import (
    DescuentoVolumen,
    PrecioNormal,
    PrecioVIP,
    PricingService,
)


def make_order(order_id: int = 1, cantidad: int = 1) -> Order:
    return Order(
        id=order_id,
        cliente="Test",
        articulos=[Item(nombre="Laptop", precio=10000, cantidad=cantidad)],
    )


# --- Strategy ---
def test_precio_normal():
    service = PricingService(PrecioNormal())
    assert service.calcular_precio(make_order()) == 10000


def test_descuento_volumen_aplicado():
    service = PricingService(DescuentoVolumen(min_items=5, descuento=0.15))
    order = make_order(cantidad=5)
    assert service.calcular_precio(order) == 10000 * 5 * 0.85


def test_descuento_volumen_no_aplicado():
    service = PricingService(DescuentoVolumen(min_items=5, descuento=0.15))
    order = make_order(cantidad=2)
    assert service.calcular_precio(order) == 20000


def test_precio_vip():
    service = PricingService(PrecioVIP(descuento=0.20))
    assert service.calcular_precio(make_order()) == 8000


def test_cambiar_estrategia():
    service = PricingService(PrecioNormal())
    assert service.calcular_precio(make_order()) == 10000
    service.cambiar_estrategia(PrecioVIP(descuento=0.20))
    assert service.calcular_precio(make_order()) == 8000


# --- Decorator Cache ---
def test_cache_hit():
    repo = MemoryOrderRepository()
    cached = CachedOrderRepository(repo)
    order = make_order(0)
    saved = cached.guardar(order)
    resultado1 = cached.obtener_por_id(saved.id)
    resultado2 = cached.obtener_por_id(saved.id)
    assert resultado1 == resultado2


def test_cache_invalida_al_eliminar():
    repo = MemoryOrderRepository()
    cached = CachedOrderRepository(repo)
    saved = cached.guardar(make_order(0))
    cached.eliminar(saved.id)
    assert saved.id not in cached._cache


# --- Adapter ---
def test_adapter_convierte_formato_externo():
    adapter = ExternalProviderAdapter()
    external = ExternalProviderOrder(
        {
            "order_number": "EXT-42",
            "customer_name": "Juan Perez",
            "line_items": [
                {"product_name": "Laptop", "unit_price": "15000.00", "qty": "1"},
                {"product_name": "Mouse", "unit_price": "300.00", "qty": "2"},
            ],
        }
    )
    order = adapter.to_domain(external)
    assert order.id == 42
    assert order.cliente == "Juan Perez"
    assert order.calcular_total() == 15600


def test_adapter_multiples_items():
    adapter = ExternalProviderAdapter()
    external = ExternalProviderOrder(
        {
            "order_number": "EXT-99",
            "customer_name": "Maria Lopez",
            "line_items": [
                {"product_name": "Monitor", "unit_price": "4000.00", "qty": "2"},
            ],
        }
    )
    order = adapter.to_domain(external)
    assert order.calcular_total() == 8000
