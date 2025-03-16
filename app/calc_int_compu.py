# import dash
# import locale
# import webview
# import tkinter as tk
# import plotly.graph_objects as go
# import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc

# from tkinter import filedialog
# from dash import html, Input, Output, State, callback, dcc, ALL


def format_currency(amount):

    """
    Formatea un valor numérico como moneda con símbolo de dólar.
    
    Args:
        amount (float): Cantidad a formatear.
        
    Returns:
        str: Cadena formateada con el símbolo de dólar, separador de miles y dos decimales.
    """

    return '${:,.2f}'.format(amount)


def calc_por_inter(P, p, n):
    """
    Calcula la tasa de interés periódica a partir del monto inicial, monto final y número de períodos.
    
    Args:
        P (float): Monto inicial o principal.
        p (float): Monto final o valor futuro.
        n (float): Número de períodos.
        
    Returns:
        float: Tasa de interés periódica en porcentaje.
    """
    return ((p/P)**(1/n)-1)*100


def ted_tea(tasa_diaria):
    """
    Convierte una Tasa Efectiva Diaria (TED) a Tasa Efectiva Anual (TEA).
    
    Args:
        tasa_diaria (float): Tasa efectiva diaria en porcentaje.
        
    Returns:
        float: Tasa efectiva anual en porcentaje.
    """
    # Conversor de tasa efectiva diaria a tasa efectiva anual
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**days - 1)*100


def tea_ted(tasa_anual):
    """
    Convierte una Tasa Efectiva Anual (TEA) a Tasa Efectiva Diaria (TED).
    
    Args:
        tasa_anual (float): Tasa efectiva anual en porcentaje.
        
    Returns:
        float: Tasa efectiva diaria en porcentaje.
    """
    
    days = 365 # * Año de 365 días *
    return ((1 + tasa_anual/100)**(1/days) - 1)*100


def tem_tea(tasa_mensual):
    """
    Convierte una Tasa Efectiva Mensual (TEM) a Tasa Efectiva Anual (TEA).
    
    Args:
        tasa_mensual (float): Tasa efectiva mensual en porcentaje.
        
    Returns:
        float: Tasa efectiva anual en porcentaje.
    """
    
    return ((1 + tasa_mensual/100)**12 - 1)*100


def tea_tem(tasa_anual):
    """
    Convierte una Tasa Efectiva Anual (TEA) a Tasa Efectiva Mensual (TEM).
    
    Args:
        tasa_anual (float): Tasa efectiva anual en porcentaje.
        
    Returns:
        float: Tasa efectiva mensual en porcentaje.
    """
    
    return ((1 + tasa_anual/100)**(1/12) - 1)*100


def tem_ted(tasa_mensual):
    """
    Convierte una Tasa Efectiva Mensual (TEM) a Tasa Efectiva Diaria (TED).
    
    Args:
        tasa_mensual (float): Tasa efectiva mensual en porcentaje.
        
    Returns:
        float: Tasa efectiva diaria en porcentaje.
    """

    days = 365 # * Año de 365 días *
    return ((1 + tasa_mensual/100)**(12/days) - 1)*100


def ted_tem(tasa_diaria):
    """
    Convierte una Tasa Efectiva Diaria (TED) a Tasa Efectiva Mensual (TEM).
    
    Args:
        tasa_diaria (float): Tasa efectiva diaria en porcentaje.
        
    Returns:
        float: Tasa efectiva mensual en porcentaje.
    """
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**(days/12) - 1)*100


def calc_interes(P, r, n):
    """
    Calcula el monto final de una inversión o préstamo con interés compuesto.
    
    Args:
        P (float): Monto inicial o principal.
        r (float): Tasa de interés periódica en porcentaje.
        n (float): Número de períodos.
        
    Returns:
        float: Monto final después de n períodos.
    """

    return P*(1 + r/100)**n

# Capex: cap
# Opex: opex
# Producción: energy
# r: tasa de descuento
# n: años de vida útil del proyecto

def calc_lcoe(cap, ope, energy, r, n):
    """
    Cálculo del Costo Nivelado de la Energía (LCOE), que es el costo promedio por unidad-
    de energía producida durante la vida útil de un proyecto de energía.
    Este dato se usa para comparar el costo de producir electricidad con diferentes tecnologías.

    Args:
        cap (float): Costo de inversión (Capex) en millones de dólares.
        ope (float): Costos operativos (Opex) anuales en millones de dólares.
        energy (float): Producción anual de energía en MWh.
        r (float): Tasa de descuento anual (ejemplo 0.05 para 5%).
        n (int): Años de vida útil del proyecto.

    Returns:
        float: Costo Nivelado de la Energía (LCOE) en dólares por MWh.
    """

    # Inicializando acumuladores
    costos_descontados = 0
    produccion_descontada = 0

    for t in range(0, n+1):

        f_desc = (1 + r)**t
        # Sumar CAPEX solo en el primer año, OPEX en todos los años
        costos_anuales = (cap if t == 0 else 0) + (ope if t != 0 else 0)
        # Costos descontados
        costos_descontados += costos_anuales/f_desc
        # Sumar la producción de cada año 
        if t != 0:
            produccion_descontada += energy/f_desc

    lcoe = costos_descontados/produccion_descontada
    return lcoe


# ------------------    Test area ----------------------
# # Calcular interese de producción para el cucho
# p = 2420000
# P = 2400000
# n = 1
# intermensual = calc_por_inter(P, p, n)
# print(intermensual)
# interanual = tea_tem(intermensual)
# inver = calc_interes(P, tea_ted(10), 34)
# print(inver)
# inter = 0.03348988954992027
# print(inter)
# inter = ted_tem(inter)
# print(inter)
# inter = tem_tea(inter)
# print(inter)
# inter = 0.03348988954992027
# inter = ted_tea(inter)
# print(inter)

# # Capital inicial
# cap_ini = 2400000
# # Numero de abonos
# num_abon = 365
# # Tasa Efectiva anual
# tea = 13
# inter = tea_tem(10)
# print(inter)
# inver = calc_interes(cap_ini, inter, 6)
# print(inver)

# # Cap inicial
# cap_ini = 2000000
# tea = 13
# inter = ted_tea(tea)
# inter = tem_tea(tea)
# print(inter)
# inver = calc_interes(cap_ini, inter, 1)

# print(inver)


# # Calculo inversiones en dolares
# Cap_ini = 2000000
# DolCap_ini = Cap_ini/4237*(1-0.9/100)
# print(DolCap_ini)
# inv_pesos = calc_interes(Cap_ini, 13, 1)
# print(inv_pesos)
# inv_usd = calc_interes(DolCap_ini, 10, 1)
# print(inv_usd)
# doltocop = inv_usd*4237

# print("inversión en pesos: ", inv_pesos*(1-9.28/100))
# print("inversión en dolar: ", doltocop*(1-3.4/100)*(1-0.9/100))


# -------------------------------------------------------

# locale.setlocale(locale.LC_ALL, 'C')
# # ----------- Dashboard ------------------
# app = dash.Dash(
#     __name__,
#     external_stylesheets=[dbc.themes.BOOTSTRAP]
# )


# server = app.server

# navbar = dbc.NavbarSimple(
    
#     brand="Luchosky",
#     color="primary",
#     dark=True,
# )

# app.layout = html.Div([
#     navbar,
#     dbc.Container([
#         dbc.Row(dbc.Col(html.Center(html.H1('Calculadora de inversiones')))),
#         dbc.Row([
#             dbc.Col([html.Center(html.H3("Ingrese el valor de la inversion: "))]),
#             dbc.Col([dbc.Input(type="number", min=0, step=0.1, id="input-inver", debounce=True),]),
#         ]),
#         dbc.Row([
#             dbc.Col([html.Center(html.H3("Ingrese el porcentaje de capitalizacion: "))]),
#             dbc.Col([dbc.Input(type="number", min=0, step=0.01, id="input-cap"),]),
#             dbc.Col([
#                 dbc.Select(
#                     [
#                         "Efectivo anual",
#                         "Efectivo mensual",
#                         "Efectivo diario",
#                         "- Otro -",
#                     ], "Efectivo anual", id="input-tip-cap",
#                 ),
#             ]),
#         ]),

#         dbc.Row([
#             dbc.Col([html.Center(html.H3("Ingrese el tiempo de inversion: "))]),
#             dbc.Col([dbc.Input(type="number", min=1, step=1),]),
#             dbc.Col([
#                 dbc.Select([
#                         "días",
#                         "meses",
#                         "años",
#                     ], "días", id="select-tiempo",
#                 ),
#             ]),
#         ]),
#     ]),
#     dbc.Container([
#         html.H4('cha', id='output')
#     ])
# ])


# @callback(
#     Output('output', "children"),
#     Output('input-inver', "value"),
#     State('input-inver', "value"),
    
#     Input('select-tiempo', "value"),
#     prevent_initial_call=True
# )
# def update_output(input1, select):
#     print('state')



# if __name__ == '__main__' :
#     # webview.create_window('Dashboard', server, maximized=True)
#     # webview.start()
#     app.run_server(debug=True)

if __name__ == '__main__' :

        ###################### Formateo de numeros a moneda ######################

    monto = 1234.56
    print(format_currency(monto))  # Resultado: "$1,234.56"

    ######################################################################################

        ###################### Tasa de interes porcentual ######################

    capital_inicial = 1000 
    capital_final = 1210
    tiempo_en_años = 2

    tasa_de_interes = calc_por_inter(capital_inicial, capital_final, tiempo_en_años)
    print(f"Tasa de interés: {tasa_de_interes:.2f}%")  # Output: 10.00%

    #####################################################################################

    ###################### Tasa efectiva diaria a tasa efectiva anual ######################

    tasa_diaria = 0.03  # 0.03% diario
    tasa_anual = ted_tea(tasa_diaria)
    print(f"TEA: {tasa_anual:.2f}%")  # Resultado: "TEA: 11.57%"

    #####################################################################################

    ###################### Tasa efectiva anual a tasa efectiva diaria ######################

    tasa_anual = 10  # 10% anual
    tasa_diaria = tea_ted(tasa_anual)
    print(f"TED: {tasa_diaria:.4f}%")  # Resultado: "TED: 0.0261%"

    #####################################################################################

    ###################### Tasa efectiva mesual a tasa efectiva anual ######################

    tasa_mensual = 1  # 1% mensual
    tasa_anual = tem_tea(tasa_mensual)
    print(f"TEA: {tasa_anual:.2f}%")  # Resultado: "TEA: 12.68%"

    #####################################################################################

    ###################### Tasa efectiva anual a tasa efectiva mesual ######################

    tasa_anual = 12  # 12% anual
    tasa_mensual = tea_tem(tasa_anual)
    print(f"TEM: {tasa_mensual:.2f}%")  # Resultado: "TEM: 0.95%"

    #####################################################################################

    ###################### Tasa efectiva mensual a tasa efectiva diaria ######################

    tasa_mensual = 1  # 1% mensual
    tasa_diaria = tem_ted(tasa_mensual)
    print(f"TED: {tasa_diaria:.4f}%")  # Resultado: "TED: 0.0329%"

    #####################################################################################

    ###################### Tasa efectiva diaria a tasa efectiva mesual ######################

    tasa_diaria = 0.03  # 0.03% diario
    tasa_mensual = ted_tem(tasa_diaria)
    print(f"TEM: {tasa_mensual:.2f}%")  # Resultado: "TEM: 0.92%"

    #####################################################################################

    ###################### Calculo del interes compuesto ######################

    capital = 1000
    tasa = 5  # 5% 
    periodos = 3  # años
    monto_final = calc_interes(capital, tasa, periodos)
    print(format_currency(monto_final))  # Resultado: "$1,157.63"

    #####################################################################################

    ########## LCOE (Levelized Cost of Energy) o Costo Nivelado de Energía ##########

    # Ejemplo: proyecto solar
    capex = 1000 # $1k de inversión inicial
    opex = 100    # $100 de costos operativos anuales
    energia_anual = 500  # 500 Wh generados por año
    tasa_descuento = 0.1   # 10% de tasa de descuento
    vida_util = 3          # 3 años de vida útil

    lcoe = calc_lcoe(capex, opex, energia_anual, tasa_descuento, vida_util)
    print(f"El LCOE del proyecto es: ${lcoe:.4f} por MWh")