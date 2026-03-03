from sqlalchemy.orm import Session

from app.infrastructure.database.models import OrderItemModel, OrderModel, User
from app.utils.logger import get_logger

logger = get_logger(__name__)


def crear_usuario(session: Session, nombre: str, email: str) -> User:
    user = User(nombre=nombre, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info("Usuario creado: %s", user)
    return user


def obtener_usuario(session: Session, user_id: int) -> User | None:
    user = session.get(User, user_id)
    logger.debug("Usuario obtenido: %s", user)
    return user


def obtener_todos_usuarios(session: Session) -> list[User]:
    users = session.query(User).all()
    logger.debug("Usuarios obtenidos: %d", len(users))
    return users


def crear_orden(session: Session, user_id: int, items: list[dict]) -> OrderModel:
    order = OrderModel(user_id=user_id)
    session.add(order)
    session.flush()

    for item in items:
        order_item = OrderItemModel(
            order_id=order.id,
            nombre=item["nombre"],
            precio=item["precio"],
            cantidad=item["cantidad"],
        )
        session.add(order_item)

    session.commit()
    session.refresh(order)
    logger.info("Orden creada: %s con %d items", order, len(items))
    return order


def obtener_orden(session: Session, order_id: int) -> OrderModel | None:
    order = session.get(OrderModel, order_id)
    logger.debug("Orden obtenida: %s", order)
    return order


def obtener_ordenes_por_usuario(session: Session, user_id: int) -> list[OrderModel]:
    orders = session.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    logger.debug("Ordenes para user_id=%d: %d encontradas", user_id, len(orders))
    return orders


def eliminar_orden(session: Session, order_id: int) -> bool:
    order = session.get(OrderModel, order_id)
    if not order:
        logger.warning("Orden %d no encontrada para eliminar", order_id)
        return False
    session.delete(order)
    session.commit()
    logger.info("Orden %d eliminada", order_id)
    return True
