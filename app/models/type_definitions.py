from typing import Protocol, TypedDict, runtime_checkable


class ArticuloDict(TypedDict):
    nombre: str
    precio: float
    cantidad: int


@runtime_checkable
class Calculable(Protocol):
    id: int
    articulos: list

    def calcular_total(self) -> float: ...

    def es_valido(self) -> bool: ...
