from pydantic import BaseModel, field_validator


class ItemIn(BaseModel):
    nombre: str
    precio: float
    cantidad: int

    @field_validator("precio")
    def precio_positivo(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("cantidad")
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v


class OrderIn(BaseModel):
    id: int
    cliente: str
    articulos: list[ItemIn]

    @field_validator("cliente")
    def cliente_valido(cls, v):
        if not v.strip():
            raise ValueError("El cliente no puede estar vacio")
        return v


class ItemOut(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    subtotal: float


class OrderOut(BaseModel):
    id: int
    cliente: str
    articulos: list[ItemOut]
    total: float
