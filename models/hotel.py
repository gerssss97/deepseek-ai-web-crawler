from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ComboPrecio(BaseModel):
    titulo: str
    descripcion: str  
    precio: float     

class Habitacion(BaseModel):
    nombre: str
    detalles: Optional[str]
    combos: List[ComboPrecio]

class Hotel(BaseModel):
    habitacion: List[Habitacion]
    detalles: str


class ParametrosBusqueda(BaseModel):
    fecha_entrada: date
    fecha_salida: date
    adultos: int
    ninos: int
