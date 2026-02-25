from app.models.item import Item
from app.models.order import Order
from app.models.order_schemas import ItemOut, OrderIn, OrderOut


def order_in_to_entity(order_in: OrderIn) -> Order:
    articulos: list[Item] = [
        Item(nombre=a.nombre, precio=a.precio, cantidad=a.cantidad)
        for a in order_in.articulos
    ]
    return Order(id=order_in.id, cliente=order_in.cliente, articulos=articulos)


def entity_to_order_out(order: Order) -> OrderOut:
    articulos_out: list[ItemOut] = [
        ItemOut(
            nombre=item.nombre,
            precio=item.precio,
            cantidad=item.cantidad,
            subtotal=item.subtotal(),
        )
        for item in order.articulos
    ]
    return OrderOut(
        id=order.id,
        cliente=order.cliente,
        articulos=articulos_out,
        total=order.calcular_total(),
    )
