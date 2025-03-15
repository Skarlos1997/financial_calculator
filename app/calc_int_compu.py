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
    return '${:,.2f}'.format(amount)


def calc_por_inter(P, p, n):
    return ((p/P)**(1/n)-1)*100


def ted_tea(tasa_diaria):
    # Conversor de tasa efectiva diaria a tasa efectiva anual
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**days - 1)*100


def tea_ted(tasa_anual):
    # Conversor de tasa efectiva anual a tasa efectiva diaria
    days = 365 # * Año de 365 días *
    return ((1 + tasa_anual/100)**(1/days) - 1)*100


def tem_tea(tasa_mensual):
    # Conversor de tasa efectiva mensual a tasa efectiva anual
    return ((1 + tasa_mensual/100)**12 - 1)*100


def tea_tem(tasa_anual):
    # Conversor de tasa efectiva anual a tasa efectiva mensual
    return ((1 + tasa_anual/100)**(1/12) - 1)*100


def tem_ted(tasa_mensual):
    # Conversor de tasa efectiva mensual a tasa efectiva diaria
    days = 365 # * Año de 365 días *
    return ((1 + tasa_mensual/100)**(12/days) - 1)*100


def ted_tem(tasa_diaria):
    # Conversor de tasa efectiva diaria a tasa efectiva mensual
    days = 365 # * Año de 365 días *
    return ((1 + tasa_diaria/100)**(days/12) - 1)*100


def calc_interes(P, r, n):
    return P*(1 + r/100)**n


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

# Capital inicial
cap_ini = 2400000
# Numero de abonos
num_abon = 365
# Tasa Efectiva anual
tea = 13
inter = tea_tem(10)
print(inter)
inver = calc_interes(cap_ini, inter, 6)
print(inver)

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
