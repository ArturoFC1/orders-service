from pydantic import BaseModel, field_validator


class ItemDTO(BaseModel):
    nombre: str
    precio: float
    cantidad: int

    @field_validator("precio")
    def precio_positivo(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("cantidad")
    def cantidad_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v


class CreateOrderDTO(BaseModel):
    cliente: str
    items: list[ItemDTO]

    @field_validator("cliente")
    def cliente_valido(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El cliente no puede estar vacio")
        return v


class OrderResponseDTO(BaseModel):
    id: int
    cliente: str
    total: float
    items: list[ItemDTO]
