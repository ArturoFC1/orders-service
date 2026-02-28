from app.adapters.memory_order_repository import MemoryOrderRepository
from app.models.item import Item
from app.models.order import Order
from app.ports.order_repository import OrderRepositoryPort
from app.services.order_domain_service import OrderDomainService


def make_order(order_id: int = 1) -> Order:
    return Order(
        id=order_id,
        cliente="Test",
        articulos=[Item(nombre="Laptop", precio=15000, cantidad=1)],
    )


# --- Verificacion LSP ---
def test_memory_repository_cumple_protocolo():
    repo = MemoryOrderRepository()
    assert isinstance(repo, OrderRepositoryPort)


# --- Tests con implementacion en memoria ---
def test_guardar_y_obtener_orden():
    repo = MemoryOrderRepository()
    service = OrderDomainService(repo)
    order = make_order(0)
    saved = service.guardar(order)
    assert saved.id == 1
    assert service.obtener_por_id(1) is not None


def test_obtener_todas_ordenes():
    repo = MemoryOrderRepository()
    service = OrderDomainService(repo)
    service.guardar(make_order(0))
    service.guardar(make_order(0))
    assert len(service.obtener_todas()) == 2


def test_eliminar_orden():
    repo = MemoryOrderRepository()
    service = OrderDomainService(repo)
    saved = service.guardar(make_order(0))
    result = service.eliminar(saved.id)
    assert result is True
    assert service.obtener_por_id(saved.id) is None


def test_orden_no_encontrada():
    repo = MemoryOrderRepository()
    service = OrderDomainService(repo)
    assert service.obtener_por_id(999) is None


def test_total_vendido():
    repo = MemoryOrderRepository()
    service = OrderDomainService(repo)
    service.guardar(make_order(0))
    service.guardar(make_order(0))
    assert service.total_vendido() == 30000.0


# --- Verificacion DIP: el servicio acepta cualquier implementacion ---
def test_servicio_acepta_cualquier_repositorio():
    class MockRepository:
        def obtener_todos(self) -> list[Order]:
            return [make_order(1)]

        def obtener_por_id(self, order_id: int) -> Order | None:
            return make_order(order_id)

        def guardar(self, order: Order) -> Order:
            return order

        def eliminar(self, order_id: int) -> bool:
            return True

    service = OrderDomainService(MockRepository())
    assert len(service.obtener_todas()) == 1
    assert service.total_vendido() == 15000.0
