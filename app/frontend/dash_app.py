import dash
import requests
from dash import html, dcc, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd  # Para manipulación de datos
import numpy as np  # Para operaciones numéricas
import dash_bootstrap_components as dbc  # Bootstrap components para mejorar la interfaz
# Importa las funciones de layouts y callbacks
from layouts import get_inicio_layout, get_lcoe_layout, get_interes_compuesto_layout, get_conversion_tasa_layout, get_historial_lcoe_layout, get_historial_interes_compuesto_layout,register_all_callbacks

# ==============================================================================
# Inicializar la aplicación Dash con un tema de Bootstrap
# ==============================================================================
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)

register_all_callbacks(app)

server = app.server

# Crea los layouts
inicio_layout = get_inicio_layout()
lcoe_layout = get_lcoe_layout()
interes_compuesto_layout = get_interes_compuesto_layout()
conversion_tasa_layout = get_conversion_tasa_layout()
historial_lcoe_layout = get_historial_lcoe_layout()
historial_interes_compuesto_layout = get_historial_interes_compuesto_layout()

# ------------------------------------------------------------------------------
# URLs de imagenes externas
# ------------------------------------------------------------------------------

imagenes = {}
imagenes['logo'] = ''

# ==============================================================================
# Definiendo el layout para el contenido dinamico (multipagina)
# ==============================================================================

app.layout = html.Div(
    [
        dbc.Container(
            [
                # Barra de navegación
                dbc.NavbarSimple(
                    brand=dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/logo.png", height="50px")),
                            dbc.Col(dbc.NavItem(dbc.NavLink("Calculadora Financiera", href="/"))),
                        ], className="ml-auto",
                        align="center",
                    ),
                    color="primary",
                    dark=True,
                    children=[
                        dbc.NavItem(dbc.NavLink("Inicio", href="/", active="exact"), id = "nav-inicio"),
                        dbc.Tooltip("Ir a la página principal",target = "nav-inicio"),
                        dbc.NavItem(dbc.NavLink("LCOE", href="/lcoe", active="exact"), id = "nav-lcoe"),
                        dbc.Tooltip("Ir a la página de LCOE",target = "nav-lcoe"),
                        dbc.NavItem(dbc.NavLink("Interés Compuesto", href="/interes-compuesto", active="exact"), id = "nav-interes-compuesto"),
                        dbc.Tooltip("Ir a la página de interés compuesto",target = "nav-interes-compuesto"),
                        dbc.NavItem(dbc.NavLink("Conversión Tasa de Interes", href="/conversion_tasa", active="exact"), id = "nav-conversion-tasa"),
                        dbc.Tooltip("Ir a la página de conversión tasa de interés",target = "nav-conversion-tasa"),
                        dbc.DropdownMenu(
                            label = "Historial",
                            nav = True, # indicando que es un componente del Nav
                            in_navbar = True, # indicando que se encuentra en la barra de navegación
                            align_end=True,
                            children = [
                                dbc.DropdownMenuItem("Hisotial de LCOE", href = "/historial-lcoe"),
                                dbc.DropdownMenuItem("Historial de Interés Compuesto", href = "/historial-interes-compuesto")
                            ],
                            id = "nav-historial",
                        ),
                        dbc.Tooltip("Ir a la página de historial",target = "nav-historial")
                    ],
                    style={"fontFamily": "Arial"}
                ),
                
                dcc.Location(id="url", refresh=False),  # Componente para rastrear la URL

                # Contenedor del contenido con flex para ocupar el espacio disponible
                html.Div(
                    id="page-content", 
                    style={"padding": "20px", "flex": "1"}
                ),
            ],
            fluid=True,
            style={"flex": "1"}
        ),

        # Pie de página siempre al final
        html.Footer(
            dbc.Row(
                [
                    dbc.Col(html.P("© 2025 Mi Aplicación Financiera"), width=4),
                    dbc.Col(html.P("Email: info@miaplicacionfinanciera.com"), width=4),
                    dbc.Col(html.P("Teléfono: +1 234 567 890"), width=4),
                ],
                justify="center",
                align="center",
                style={"margin": "0"}
            ),
            style={
                "textAlign": "center", 
                "padding": "20px", 
                "backgroundColor": "#f8f9fa"
            }
        )
    ],
    style={
        "minHeight": "100vh",        # Altura mínima de la ventana
        "display": "flex",           # Utiliza Flexbox
        "flexDirection": "column",    # Organiza en columna
        "fontFamily": "Helvetica, sans-serif",
        "color": "#333"
    }
)



# ------------------------------------------------------------------------------
# Callback para cambiar el contenido según la URL
# ------------------------------------------------------------------------------

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return inicio_layout
    elif pathname == "/lcoe":
        return lcoe_layout
    elif pathname == "/interes-compuesto":
        return interes_compuesto_layout
    elif  pathname == "/conversion_tasa":
        return conversion_tasa_layout
    elif pathname == "/historial-lcoe":
        return historial_lcoe_layout
    elif pathname == "/historial-interes-compuesto":
        return historial_interes_compuesto_layout
    else:
        return dbc.Alert("Página no encontrada.", color="danger")

if __name__ == '__main__':
    app.run(debug=True, port=8050)