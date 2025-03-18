from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy.orm import Session
from calc_int_compu import *
from database import SessionLocal
from models import *

app = FastAPI(title="Calculadora Financiera API", 
              description="API para realizar cálculos financieros")

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint ventana principal
@app.get("/")
def inicio():
    contenido = """ 
                <h1>Calculadora Financiera</h1>
                <hr>
                <p>Esta es una calculadora financiera básica que te permite realizar cálculos de interés simple y compuesto, así como conversiones de tasas de interés.</p>
                <p>Explora la <a href="/docs">documentación de la API</a> para más detalles.</p>
                """
    return HTMLResponse(content=contenido)

# Endpoin calculo de conversor de tasa de interes
@app.post("/convertir-tasas")
def calcular_interes(request: ConversionTasaRequest):
    tasa = request.tasa
    tipo = request.tipo

    # Primero se pasa a tasa anual para luego pasar a cualquier otro tipo
    if tipo == TipoTasa.DIARIO:
        tasa_anual = ted_tea(tasa)
    elif tipo == TipoTasa.MENSUAL:
        tasa_anual = tem_tea(tasa)
    else:
        tasa_anual = tasa

    # Luego convertimos a las otras tasas
    tasa_diaria = tea_ted(tasa_anual)
    tasa_mensual = tea_tem(tasa_anual)

    return ConversionTasaResponse(
        tasa_diaria = round(tasa_diaria, 6),
        tasa_mensual = round(tasa_mensual, 4),
        tasa_anual = round(tasa_anual, 2),
        mensaje = f"Tasa {tipo.value} de {tasa}% equivale a {round(tasa_anual, 2)}% anual"
    )

# Enpoint Calculo de interes compuesto
@app.post("/interes-compuesto")
def calcular_interes_compuesto(request: InteresCompuestoRequest, db: Session = Depends(get_db)):
    capital = request.capital
    tasa = request.tasa
    plazo = request.plazo
    tipo_tasa = request.tipo_tasa

    # Convertir tasa a la frecuencia correcta segun el plazo
    tasa_anual = 0
    if tipo_tasa == TipoTasa.DIARIO:
        tasa_anual = ted_tea(tasa)
    elif tipo_tasa == TipoTasa.MENSUAL:
        tasa_anual = tem_tea(tasa)
    else:
        tasa_anual = tasa
    
    # Calculo del interes compuesto segun el tipo de plazo
    # Plazo en dias
    if tipo_tasa == TipoTasa.DIARIO:
        monto_final = calc_interes(capital, tasa, plazo)
    # Plazo en meses
    elif tipo_tasa == TipoTasa.MENSUAL:
        monto_final = calc_interes(capital, tasa, plazo)
        # Plazo en años
    else:
        monto_final = calc_interes(capital, tasa, plazo)
    
    ganancias = monto_final - capital

    # Guardar en la base de datos
    nuevo_calculo = InteresCompuestoDB(capital=capital, tasa=tasa, plazo=plazo, monto_final=monto_final, ganancias=ganancias)
    db.add(nuevo_calculo)
    db.commit()
    db.refresh(nuevo_calculo)

    return {
        "capital_inicial": format_currency(capital),
        "tasa_aplicada": f"{tasa}% {tipo_tasa.value}",
        "tasa_anual_equivalente": f"{round(tasa_anual, 2)}%",
        "plazo": f"{plazo} periodos ({tipo_tasa.value})",
        "monto_final": format_currency(monto_final),
        "ganancias": format_currency(ganancias)
    }

# Endpoint para calcular el costo nivelado de la energía (LCOE)
@app.post("/lcoe")
def calcular_lcoe(request: LCOERequest):
    capex = request.capex
    opex = request.opex
    produccion_anual = request.produccion_anual
    tasa_descuento = request.tasa_descuento
    vida_util = request.vida_util
    # Calculo del LCOE
    lcoe = calc_lcoe(capex, opex, produccion_anual, tasa_descuento, vida_util)
    return {
        "lcoe": round(lcoe, 2),
        "unidad": "$/MWh",
        "mensaje": f"El costo nivelado de la energía es {round(lcoe, 2)} $/MWh"
    }

# Endpoints para actualizar y eliminar datos de la base de datos para el calculo de interes compuesto

@app.put("/interes-compuesto/{id}")
def actualizar_calculo(id: int, request: InteresCompuestoRequest, db: Session = Depends(get_db)):
    calculo = db.query(InteresCompuestoDB).filter(InteresCompuestoDB.id == id).first()
    if not calculo:
        return {"error": "Cálculo no encontrado"}

    # Actualizar valores
    calculo.capital = request.capital
    calculo.tasa = request.tasa
    calculo.plazo = request.plazo
    calculo.monto_final = calc_interes(request.capital, request.tasa, request.plazo)
    calculo.ganancias = calculo.monto_final - request.capital

    db.commit()
    db.refresh(calculo)
    return {"mensaje": "Cálculo actualizado", "datos": calculo}

@app.delete("/interes-compuesto/{id}")
def eliminar_calculo(id: int, db: Session = Depends(get_db)):
    calculo = db.query(InteresCompuestoDB).filter(InteresCompuestoDB.id == id).first()
    if not calculo:
        return {"error": "Cálculo no encontrado"}

    db.delete(calculo)
    db.commit()
    return {"mensaje": f"Cálculo con ID {id} eliminado correctamente"}

# Endpoints para actualizar y eliminar datos del calculo de LCOE

@app.put("/lcoe/{id}")
def actualizar_lcoe(id: int, request: LCOERequest, db: Session = Depends(get_db)):
    lcoe = db.query(LCOEDB).filter(LCOEDB.id == id).first()
    if not lcoe:
        return {"error": "LCOE no encontrado"}
    
    # Actualizando los valores
    lcoe.capex = request.capex
    lcoe.opex = request.opex
    lcoe.produccion_anual = request.produccion_anual
    lcoe.tasa_descuento = request.tasa_descuento
    lcoe.vida_util = request.vida_util

    db.commit()
    db.refresh(lcoe)
    return {"mensaje": "LCOE actualizado", "datos": lcoe}

@app.delete("/lcoe/{id}")
def eliminar_lcoe(id: int, db: Session = Depends(get_db)):
    lcoe = db.query(LCOEDB).filter(LCOEDB.id == id).filter(LCOEDB.id == id).first()
    if not lcoe:
        return {"error": "LCOE no encontrado"}
    
    db.delete(lcoe)
    db.commit()
    return {"mensaje": f"LCOE con ID {id} eliminado correctamente"}