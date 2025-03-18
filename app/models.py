from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy import Column, Integer, Float
from database import Base

class InteresCompuestoDB(Base):
    __tablename__ = "interes_compuesto"
    id = Column(Integer, primary_key=True, index=True)
    capital = Column(Float, nullable=False)
    tasa = Column(Float, nullable=False)
    plazo = Column(Integer, nullable=False)
    monto_final = Column(Float, nullable=False)
    ganancias = Column(Float, nullable=False)

# Modelos de datos para la conversión de tasas
class TipoTasa(str, Enum):
    # Tipos de tasa de interés
    ANUAL = "anual"
    MENSUAL = "mensual"
    DIARIO = "diario"

class ConversionTasaRequest(BaseModel):
    # Campo obligatorio: valor de la tasa
    tasa: float = Field(..., description="Valor de la tasa", gt=0)
    # Campo obligatorio: tipo de tasa
    tipo: TipoTasa = Field(..., description="Tipo de tasa")

class ConversionTasaResponse(BaseModel):
    tasa_diaria: float
    tasa_mensual: float
    tasa_anual: float
    mensaje: str

# Modelos de datos para el calculo de interés compuesto
class InteresCompuestoRequest(BaseModel):
    # Campo obligatorio: capital inicial
    capital: float = Field(..., description = "Capital inicial", gt = 0)
    tasa: float = Field(..., description="Tasa de interés", gt=0)
    plazo: float = Field(..., description="Plazo en periodos", gt=0)
    tipo_tasa: TipoTasa = Field(..., description="Tipo de tasa (diaria, mensual, anual)")

# Modelo de datos para el cálculo del costo nivelado de la energía (LCOE)
class LCOERequest(BaseModel):
    # CAPEX: Costo inicial de inversión (solo en t = 1)
    capex: float = Field(..., description="Costo inicial de inversión en $", gt = 0)
    # OPEX: Costo operativo anual (en $/año)
    opex: float = Field(..., description="Costo operativo anual en $/año", gt = 0)
    # Producción anual (en MWh/año)
    produccion_anual: float = Field(..., description="Producción anual en MWh/año ", gt = 0)
    # Tasa de descuento
    tasa_descuento: float = Field(..., description="Tasa de descuento anual (ejemplo: 0.05 para 5%)", gt = 0)
    # Plazo de vida de la planta (en años)
    vida_util: int = Field(..., description="Plazo de vida de la planta en años", gt = 0)

