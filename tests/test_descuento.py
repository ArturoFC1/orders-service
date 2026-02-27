import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.models.item import Item
from app.models.order import Order
from app.services.descuento_service import DescuentoService

# --- TDD: tests primero ---


def make_order(items: list[dict]) -> Order:
    return Order(
        id=1,
        cliente="Test",
        articulos=[
            Item(nombre=i["nombre"], precio=i["precio"], cantidad=i["cantidad"])
            for i in items
        ],
    )


def test_descuento_aplicado_si_total_mayor_10000():
    order = make_order([{"nombre": "Laptop", "precio": 15000, "cantidad": 1}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total == 15000 * 0.90


def test_sin_descuento_si_total_menor_10000():
    order = make_order([{"nombre": "Mouse", "precio": 300, "cantidad": 2}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total == 600


def test_descuento_exacto_en_limite():
    order = make_order([{"nombre": "Item", "precio": 10000, "cantidad": 1}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total == 10000


def test_total_con_descuento_nunca_negativo():
    order = make_order([{"nombre": "Item", "precio": 0.01, "cantidad": 1}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total >= 0


@pytest.mark.parametrize(
    "precio,cantidad,esperado",
    [
        (15000, 1, 15000 * 0.90),
        (5000, 2, 10000),
        (300, 2, 600),
        (20000, 1, 20000 * 0.90),
    ],
)
def test_descuento_parametrizado(precio, cantidad, esperado):
    order = make_order([{"nombre": "Item", "precio": precio, "cantidad": cantidad}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total == esperado


# --- Property-based testing con Hypothesis ---


@given(
    precio=st.floats(
        min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False
    ),
    cantidad=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=100)
def test_total_siempre_no_negativo(precio, cantidad):
    order = make_order([{"nombre": "Item", "precio": precio, "cantidad": cantidad}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    assert total >= 0


@given(
    precio=st.floats(
        min_value=10001, max_value=1_000_000, allow_nan=False, allow_infinity=False
    ),
    cantidad=st.integers(min_value=1, max_value=10),
)
@settings(max_examples=100)
def test_descuento_siempre_menor_al_original(precio, cantidad):
    order = make_order([{"nombre": "Item", "precio": precio, "cantidad": cantidad}])
    service = DescuentoService()
    total = service.aplicar_descuento(order)
    original = order.calcular_total()
    assert total < original
