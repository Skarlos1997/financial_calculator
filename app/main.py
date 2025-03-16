from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from enum import Enum
from calc_int_compu import *
from models import *

app = FastAPI(title="Calculadora Financiera API", 
              description="API para realizar cálculos financieros")

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
def calcular_interes_compuesto(request: InteresCompuestoRequest):
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