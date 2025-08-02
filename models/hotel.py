from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date
import string

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



#######################################################


def normalizar_precio_str(s: str) -> Optional[float]:
    try:
        cleaned = s.replace("$", "").replace("€", "").replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return None

class HabitacionExcel(BaseModel):
    nombre: str
    precio_raw: Optional[str] = None
    precio: Optional[float] = None
    row_idx: int

    @validator("nombre", pre=True)
    def limpiar_nombre(cls, v):
        if v is None:
            raise ValueError("nombre no puede ser None")
        nombre = str(v).strip().lower()
        nombre = nombre.rstrip(string.punctuation + " ").strip()
        return nombre

    @validator("precio_raw", pre=True, always=True)
    def normalizar_raw(cls, v):
        if v is None:
            return None
        s = str(v).strip()
        return s if s != "" else None

    @validator("precio", pre=True, always=True)
    def set_precio(cls, v, values):
        if v is not None:
            return v
        raw = values.get("precio_raw")
        if raw is None:
            return None
        return normalizar_precio_str(raw)

class DatosExcel(BaseModel):
    tipos_habitacion_excel: List[str]
    habitaciones: List[HabitacionExcel]