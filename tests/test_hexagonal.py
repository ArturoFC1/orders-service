import pytest

from app.application.dtos.order_dtos import CreateOrderDTO, ItemDTO
from app.application.use_cases.order_use_cases import (
    CreateOrderUseCase,
    DeleteOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
)
from app.domain.entities.order import Order
from app.domain.ports.notification_port import NotificationPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)


# --- Mocks ---
class MockNotification:
    def __init__(self):
        self.notificaciones: list[Order] = []

    def notificar_orden_creada(self, order: Order) -> None:
        self.notificaciones.append(order)


# --- Verificacion de contratos (LSP) ---
def test_memory_repository_cumple_protocolo():
    repo = MemoryOrderRepository()
    assert isinstance(repo, OrderRepositoryPort)


def test_mock_notification_cumple_protocolo():
    notification = MockNotification()
    assert isinstance(notification, NotificationPort)


# --- Tests de casos de uso ---
@pytest.fixture
def repo():
    return MemoryOrderRepository()


@pytest.fixture
def notification():
    return MockNotification()


@pytest.fixture
def create_use_case(repo, notification):
    return CreateOrderUseCase(repo, notification)


def test_create_order_use_case(create_use_case, notification):
    dto = CreateOrderDTO(
        cliente="Juan Perez",
        items=[ItemDTO(nombre="Laptop", precio=15000, cantidad=1)],
    )
    result = create_use_case.execute(dto)
    assert result.id > 0
    assert result.cliente == "Juan Perez"
    assert result.total == 15000
    assert len(notification.notificaciones) == 1


def test_get_order_use_case(repo, create_use_case):
    dto = CreateOrderDTO(
        cliente="Maria Lopez",
        items=[ItemDTO(nombre="Mouse", precio=300, cantidad=2)],
    )
    created = create_use_case.execute(dto)
    use_case = GetOrderUseCase(repo)
    result = use_case.execute(created.id)
    assert result is not None
    assert result.id == created.id


def test_get_order_not_found(repo):
    use_case = GetOrderUseCase(repo)
    assert use_case.execute(999) is None


def test_list_orders_use_case(repo, create_use_case):
    create_use_case.execute(
        CreateOrderDTO(
            cliente="Juan",
            items=[ItemDTO(nombre="Laptop", precio=15000, cantidad=1)],
        )
    )
    create_use_case.execute(
        CreateOrderDTO(
            cliente="Maria",
            items=[ItemDTO(nombre="Mouse", precio=300, cantidad=2)],
        )
    )
    use_case = ListOrdersUseCase(repo)
    result = use_case.execute()
    assert len(result) == 2


def test_delete_order_use_case(repo, create_use_case):
    created = create_use_case.execute(
        CreateOrderDTO(
            cliente="Juan",
            items=[ItemDTO(nombre="Laptop", precio=15000, cantidad=1)],
        )
    )
    use_case = DeleteOrderUseCase(repo)
    assert use_case.execute(created.id) is True
    assert GetOrderUseCase(repo).execute(created.id) is None


def test_notificacion_enviada_al_crear(create_use_case, notification):
    create_use_case.execute(
        CreateOrderDTO(
            cliente="Test",
            items=[ItemDTO(nombre="Item", precio=100, cantidad=1)],
        )
    )
    assert len(notification.notificaciones) == 1
    assert notification.notificaciones[0].cliente == "Test"


def test_repositorio_intercambiable(notification):
    class OtroRepo:
        def __init__(self):
            self._orders = {}
            self._id = 1

        def obtener_todos(self) -> list[Order]:
            return list(self._orders.values())

        def obtener_por_id(self, order_id: int) -> Order | None:
            return self._orders.get(order_id)

        def guardar(self, order: Order) -> Order:
            order.id = self._id
            self._id += 1
            self._orders[order.id] = order
            return order

        def eliminar(self, order_id: int) -> bool:
            return bool(self._orders.pop(order_id, None))

    use_case = CreateOrderUseCase(OtroRepo(), notification)
    result = use_case.execute(
        CreateOrderDTO(
            cliente="Test",
            items=[ItemDTO(nombre="Item", precio=500, cantidad=2)],
        )
    )
    assert result.total == 1000
