import dash
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Definiendo la URL de la API
url_base = "http://127.0.0.1:8000"

# ------------------------------------------------------------------------------
# Layouts
# ------------------------------------------------------------------------------

def get_inicio_layout():
    return html.Div([
        html.H1("Calculadora Financiera"),
        html.P("Bienvenido a la herramienta financiera. Selecciona una opción en el menú.")
    ])

def get_lcoe_layout():
    return html.Div([
        html.H1("Cálculo de LCOE"),
        html.P("Ingresa los datos para calcular el costo nivelado de energía."),
        html.Label("CAPEX: "),
        dcc.Input(id = "input-capex", type = "number"),
        html.Br(),
        html.Label("OPEX: "),
        dcc.Input(id = "input-opex", type = "number"),
        html.Br(),
        html.Label("Producción anual (MWh): "),
        dcc.Input(id = "input-annual-production", type = "number"),
        html.Br(),
        html.Label("Tasa de descuento"),
        dcc.Input(id = "input-discount-rate", type = "number"),
        html.Br(),
        html.Label("Plazo de vida de la planta en años: "),
        dcc.Input(id = "input-project-life", type = "number"),
        html.Br(),
        html.Button('Calcular LCOE', id = 'button-lcoe', n_clicks = 0),
        html.Br(),
        html.Div(id = 'output-lcoe')
    ])

def get_interes_compuesto_layout():
    return html.Div([
        html.H1("Cálculo de Interés Compuesto"),
        html.P("Calcula el valor futuro de tu inversión."),
        html.Label("Capital inicial: "),
        dcc.Input(id = "input-capital", type = "number"),
        html.Br(),
        html.Label("Tasa de interés: "),
        dcc.Input(id = "input-tasa-interes", type = "number"),
        html.Br(),
        html.Label("Plazo en periodos (años o meses o días): "),
        dcc.Input(id = "input-plazo", type = "number"),
        html.Br(),
        html.Label("Tipo de tasa (diaria, mensual o anual)"),
        dcc.Dropdown(
            id = "dropdown-interes-compuesto", 
            options = [
                {"label": "ANUAL", "value": "anual"},
                {"label": "MENSUAL", "value": "mensual"},
                {"label": "DIARIO", "value": "diario"}
            ],
        placeholder = "Selecciona el tipo de tasa"
        ),
        html.Br(),
        html.Button("Calcular", id = "button-interes-compuesto", n_clicks = 0),
        html.Br(),
        html.Div(id = "output-interes-compuesto")
    ])

def get_conversion_tasa_layout():
    return html.Div([
        html.H1("Conversor de Tasas de Interés"),
        html.P("Convierte entre diferentes tipos de tasas de interés."),
        html.Label("Tasa (%)"),
        dcc.Input(id = "input-tasa", type = "number", placeholder = "Ingresa la tasa", debounce = True),
        html.Br(),
        html.Label("Tipo de tasa"),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "ANUAL", "value": "anual"},
                {"label": "MENSUAL", "value": "mensual"},
                {"label": "DIARIO", "value": "diario"}
            ],
            placeholder="Selecciona el tipo de tasa"
        ),
        html.Br(),
        html.Button("Convertir", id="btn-convertir", n_clicks=0),
        html.Div(id = "output-tasa")
    ])


# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------

def register_conversion_tasa_callbacks(app):
    @app.callback(
        Output("output-tasa", "children"),
        [Input("btn-convertir", "n_clicks")],
        [State("input-tasa", "value"),
         State("dropdown", "value")]
    )
    def convertir_tasas(n_clicks, tasa, tipo):
        # print(f"Callback ejecutado con n_clicks={n_clicks}, tasa={tasa}, tipo={tipo}")
        if n_clicks and tasa is not None and tipo is not None:
            # Se prepara el payload para la llamada a la API (según el modelo)
            payload = {"tasa": float(tasa), "tipo": tipo}

            try:
                # Se llama a la API
                response = requests.post("http://127.0.0.1:8000/convertir-tasas", json = payload)
                
                # Se procesa la respuesta
                if response.status_code == 200:
                    data = response.json()
                    return html.Div([
                        html.P(data.get("mensaje", "Conversión exitosa")),
                        html.P(f"Tasa Diaria: {data.get('tasa_diaria')}%"),
                        html.P(f"Tasa Mensual: {data.get('tasa_mensual')}%"),
                        html.P(f"Tasa Anual: {data.get('tasa_anual')}%")
                    ])
                else:
                    return f"Error: {response.status_code}"

            except Exception as e:
                return f"Error al conectar con el backend: {str(e)}"
        return "Ingresa los datos y presiona 'convertir'"
    
def register_interes_compuesto_callbacks(app):
    @app.callback(
        Output("output-interes-compuesto", "children"),
        [Input("button-interes-compuesto", "n_clicks")],
        [
            State("input-capital", "value"),
            State("input-tasa-interes", "value"),
            State("input-plazo", "value"),
            State("dropdown-interes-compuesto", "value")
        ]
    )
    def calcular_interes_compuesto(n_clicks, capital, tasa, plazo, tipo):
        print(f"Callback ejecutado con n_clicks={n_clicks}, capital={capital}, tasa={tasa}, plazo={plazo}, tipo={tipo}")
        if n_clicks and None not in (capital, tasa, plazo, tipo):
            # Se prepara el payload para la llamada a la API (según el modelo)
            payload = {
                "capital": float(capital),
                "tasa": float(tasa),
                "plazo": float(plazo),
                "tipo_tasa": tipo
            }

            try:
                # Se llama a la API
                response = requests.post("http://127.0.0.1:8000/interes-compuesto", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return html.Div([
                        html.P(f"Capital Inical: {data.get('capital_inicial')}"),
                        html.P(f"Tasa Aplicada: {data.get('tasa_aplicada')}"),
                        html.P(f"Tasa Anual Equivalente: {data.get('tasa_anual_equivalente')}"),
                        html.P(f"Plazo: {data.get('plazo')} años"),
                        html.P(f"Monto final: {data.get('monto_final')}"),
                        html.P(f"Ganancias: {data.get('ganancias')}"),
                    ])
                else:
                    return f"Error: {response.status_code}"
            except Exception as e:
                return f"Error al conectar con el backend: {str(e)}"
        return "Ingresa los datos y presiona 'convertir'"

def register_lcoe_callbacks(app):
    @app.callback(
        Output("output-lcoe", "children"),
        [Input("button-lcoe", "n_clicks")],
        [
            State("input-capex", "value"),
            State("input-opex", "value"),
            State("input-annual-production", "value"),
            State("input-discount-rate", "value"),
            State("input-project-life", "value")
        ]
    )
    def calcular_lcoe(n_clicks, capex, opex, annual_production, discount_rate, project_life):
        if n_clicks and None not in (capex, opex, annual_production, discount_rate, project_life):
            payload = {
                "capex": float(capex),
                "opex": float(opex),
                "produccion_anual": float(annual_production),
                "tasa_descuento": float(discount_rate),
                "vida_util": float(project_life)
            }
            try:
                response = requests.post("http://127.0.0.1:8000/lcoe", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return html.Div([
                        html.P(data.get("mensaje", "LCOE calculado correctamente")),
                    html.P(f"LCOE: {data.get('lcoe')} {data.get('unidad')}")
                    ])
                else:
                    return f"Error: {response.status_code}"
            except Exception as e:
                return f"Error al conectar con el backend: {str(e)}"
        return "Ingresa los datos y presiona 'Calcular LCOE'"

# Función para registrar todos los callbacks
def register_all_callbacks(app):
    register_conversion_tasa_callbacks(app)
    register_interes_compuesto_callbacks(app)
    register_lcoe_callbacks(app)