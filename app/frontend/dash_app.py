import dash
import requests
from dash import html, dcc, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd  # Para manipulación de datos
import numpy as np  # Para operaciones numéricas
import dash_bootstrap_components as dbc  # Bootstrap components para mejorar la interfaz
# Importa las funciones de layouts y callbacks
from layouts import get_inicio_layout, get_lcoe_layout, get_interes_compuesto_layout, get_conversion_tasa_layout, register_all_callbacks

# ==============================================================================
# Inicializar la aplicación Dash con un tema de Bootstrap
# ==============================================================================
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]  # Usar el tema Bootstrap estándar
)

register_all_callbacks(app)

server = app.server

# Crea los layouts
inicio_layout = get_inicio_layout()
lcoe_layout = get_lcoe_layout()
interes_compuesto_layout = get_interes_compuesto_layout()
conversion_tasa_layout = get_conversion_tasa_layout()

# ==============================================================================
# Definiendo el layout para el contenido dinamico (multipagina)
# ==============================================================================

app.layout = dbc.Container([
    # Barra de navegación
    dbc.NavbarSimple(
        brand = "Mi Aplicación Financiera",
        color = "primary",
        dark = True,
        children = [
            dbc.NavItem(dbc.NavLink("Inicio", href="/", active = "exact")),
            dbc.NavItem(dbc.NavLink("LCOE", href = "/lcoe", active = "exact")),
            dbc.NavItem(dbc.NavLink("Interés Compuesto", href = "/interes-compuesto", active = "exact")),
            dbc.NavItem(dbc.NavLink("Conversión Tasa de Interes", href = "/conversion_tasa", active = "exact")),
        ]
    ),

    dcc.Location(id="url", refresh=False),  # Componente para rastrear la URL
    html.Div(id="page-content")            # Contenedor para el contenido de la página

], fluid=True)


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
    else:
        return dbc.Alert("Página no encontrada.", color="danger")

if __name__ == '__main__':
    app.run(debug=True, port=8050)