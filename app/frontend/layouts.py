import dash
import requests
import pandas as pd
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
        html.H1("Calculadora Financiera", style={"textAlign": "center", "fontSize": "2.5em", "marginBottom": "20px"}),
        html.P("Bienvenido a la herramienta financiera. Selecciona una opción en el menú.", style={"color": "#555", "fontSize": "1.2em", "textAlign": "center"})
    ])

def get_lcoe_layout():
    return dbc.Container([
    html.Div([
        html.H1("Cálculo de LCOE"),
        html.P("Ingresa los datos para calcular el costo nivelado de energía para tu proyecto."),

    # Formulario con grid responsivo
    dbc.Form([
        dbc.Row([
            dbc.Col([
                html.Label("CAPEX: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-capex", type="number", value=0),
                dbc.Tooltip("Incluye costos de adquisición de terrenos, equipos, construcción, ingeniería y otros gastos relacionados con la puesta en marcha del proyecto.", target="input-capex"),
            ], md=6),
            dbc.Col([
                html.Label("OPEX: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-opex", type="number", value=0),
                dbc.Tooltip("Incluye costos de combustible, personal, mantenimiento, seguros, impuestos y otros gastos recurrentes.", target="input-opex"),
            ], md=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Label("Producción anual (MWh): ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-annual-production", type="number", value=0),
                dbc.Tooltip("Es la cantidad de energía eléctrica que la planta genera en un año, medida en megavatios hora.", target="input-annual-production"),
            ], md=6),
            dbc.Col([
                html.Label("Tasa de descuento: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-discount-rate", type="number", value=0),
                dbc.Tooltip("Representa el costo de oportunidad del capital y refleja el riesgo del proyecto.", target="input-discount-rate"),
            ], md=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Label("Plazo de vida de la planta en años: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-project-life", type="number", value=0),
                dbc.Tooltip("Es el período de tiempo durante el cual se espera que la planta genere energía de manera eficiente.", target="input-project-life"),
            ], md=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Button([html.I(className="fas fa-calculator"), " Calcular LCOE"], id="button-lcoe", n_clicks = 0,size="lg", color="primary", className="mt-3"),
                # html.Button('Reiniciar', id='button-reset', n_clicks=0, style={"marginLeft": "10px"}),
            ], md=12),
        ], className="mb-3"),
    ]),
    # Sección de resultados
    html.Div([
        dbc.Alert("Por favor, completa todos los campos.", color="danger", id="error-alert-lcoe", is_open = False),
        dcc.Loading(
            id="loading",
            type="default",
            style={"marginTop": "20px", "fontSize": "1.2em", "color": "#28a745", "textAlign": "center"},
            children=html.Div(id="output-lcoe")
            )
        ])
    ], style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "5px"})
], fluid=True, className="d-flex justify-content-center")

def get_interes_compuesto_layout():
    return dbc.Container([
        html.Div([
            # Sección de encabezado
            html.H1("Cálculo de Interés Compuesto"),
            html.P("Calcula el valor futuro de tu inversión."),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        html.Label("Capital inicial: "),
                        dcc.Input(id = "input-capital", type = "number", value=0),
                        dbc.Tooltip("Es la cantidad de dinero que inviertes o depositas al principio.",target = "input-capital"),
                    ], md = 6),

                    dbc.Col([
                        html.Label("Tasa de interés: "),
                        dcc.Input(id = "input-tasa-interes", type = "number", value=0),
                        dbc.Tooltip("Es el porcentaje que te pagan por tu dinero durante un período de tiempo.",target = "input-tasa-interes"),
                    ], md = 6),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Plazo en periodos (años o meses o días): "),
                        dcc.Input(id = "input-plazo", type = "number", value=0),
                        dbc.Tooltip("Es el tiempo que dejas tu dinero invertido.",target = "input-plazo"),
                    ], md = 6),

                    dbc.Col([
                        html.Label("Tipo de tasa (diaria, mensual o anual)"),
                        dcc.Dropdown(
                            id = "dropdown-interes-compuesto", 
                            options = [
                                {"label": "ANUAL", "value": "anual"},
                                {"label": "MENSUAL", "value": "mensual"},
                                {"label": "DIARIO", "value": "diario"}
                            ],
                        placeholder = "Selecciona el tipo de tasa",
                        style={"width": "200px"}
                        ),
                        dbc.Tooltip("Indica con qué frecuencia se añade el interés a tu capital, y esto afecta a la rapidez con la que crece tu dinero.",target = "dropdown-interes-compuesto"),
                    ], md = 6),
                ], className = "mb-3"),

                dbc.Row([
                    dbc.Col([
                        dbc.Button([html.I(className="fas fa-calculator"), "Calcular"], id="button-interes-compuesto", n_clicks = 0, size="lg", color="primary", className="mt-3"),
                    ], md = 12)
                ], className="mb-3"),
            ]),

            html.Div([
            dbc.Alert("Por favor, completa todos los campos.", color="danger", id="error-alert-ic", is_open = False),
            dcc.Loading(
                id="loading",
                type="default",
                style={"marginTop": "20px", "fontSize": "1.2em", "color": "#28a745", "textAlign": "center"},
                children=html.Div(id="output-interes-compuesto")
            )
        ])
    ], style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "5px"})
], fluid=True, className="d-flex justify-content-center")

def get_conversion_tasa_layout():
    return dbc.Container([
        html.Div([
            # Sección de encabezados
            html.H1("Conversor de Tasas de Interés"),
            html.P("Convierte entre diferentes tipos de tasas de interés."),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Tasa (%)"),
                    dcc.Input(id = "input-tasa", type = "number", placeholder = "Ingresa la tasa", debounce = True),
                    dbc.Tooltip("""Representa el "precio" del dinero, es decir, lo que se paga por usarlo (si pides un préstamo) o lo que se gana por prestarlo o invertirlo (si tienes un depósito o inversión).""",target = "input-tasa"),
                ],md = 6),
                dbc.Col([
                    html.Label("Tipo de tasa"),
                    dcc.Dropdown(
                        id="dropdown",
                        options=[
                            {"label": "ANUAL", "value": "anual"},
                            {"label": "MENSUAL", "value": "mensual"},
                            {"label": "DIARIO", "value": "diario"}
                        ],
                        placeholder="Selecciona el tipo de tasa",
                        style={"width": "200px"}
                    ),
                    dbc.Tooltip("Se refiere a la frecuencia con la que se calcula y aplica el interés a tu capital.",target = "dropdown"),
                ])
            ], className = "mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Button([html.I(className="fas fa-calculator"), "Convierte"], id="btn-convertir", n_clicks=0, size="lg", color="primary", className="mt-3")
                ], md = 6)
            ], className = "mb-3"),

            html.Div([
                dbc.Alert("Por favor, completa todos los campos.", color="danger", id="error-alert-ct", is_open = False),
                dcc.Loading(
                    id="loading",
                    type="default",
                    style={"marginTop": "20px", "fontSize": "1.2em", "color": "#28a745", "textAlign": "center"},
                    children=html.Div(id="output-ct")
                    )
            ])
        ], style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "5px"})
    ], fluid=True, className="d-flex justify-content-center")

def get_historial_lcoe_layout():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Historial de LCOE", className = "h3"),
                    dbc.CardBody([
                        html.P("Lista de registro de cálculos de LCOE"),
                        html.Div(id = "tabla-lcoe")
                    ])
                ], className="mt-4"),
                width=12
            ),
            justify = "center"
        )
    ], fluid = True)

def get_historial_interes_compuesto_layout():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Historial de interes compuesto", className = "h3"),
                    dbc.CardBody([
                        html.P("Lista de registro de cálculos de interes compuesto"),
                        html.Div(id = "tabla-ic")
                    ])
                ], className="mt-4"),
                width=12
            ),
            justify = "center"
        )
    ], fluid = True)

# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------

def register_conversion_tasa_callbacks(app):
    @app.callback(
        Output("output-ct", "children"),
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
        [Output("output-interes-compuesto", "children"),
         Output("error-alert-ic", "is_open")],
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
        if n_clicks > 0:
            if None in [capital, tasa, plazo] or any(x == 0 for x in [capital, tasa, plazo]):
                return "Ingresa los datos y presiona 'Calcular'", True  # No muestra resultado y activa el Alert
            else:
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
                            html.P(f"Plazo: {data.get('plazo')}"),
                            html.P(f"Monto final: {data.get('monto_final')}"),
                            html.P(f"Ganancias: {data.get('ganancias')}"),
                        ]), False  # Muestra resultado y desactiva el Alert
                    else:
                        return f"Error: {response.status_code}", True
                except Exception as e:
                    return f"Error al conectar con el backend: {str(e)}", True
        return "Ingresa los datos y presiona 'Calcular'", False

def register_lcoe_callbacks(app):
    @app.callback(
        [Output("output-lcoe", "children"),
         Output("error-alert-lcoe", "is_open")],
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
        if n_clicks > 0:
            if None in [capex, opex, annual_production, discount_rate, project_life] or any(x == 0 for x in [capex, opex, annual_production, discount_rate, project_life]):
                return "Ingresa los datos y presiona 'Calcular LCOE", True  # No muestra resultado y activa el Alert
            else:
                payload = {
                    "capex": float(capex),
                    "opex": float(opex),
                    "produccion_anual": float(annual_production),
                    "tasa_descuento": float(discount_rate),
                    "vida_util": float(project_life)
                }
                try:
                    response = requests.post(url_base + "/lcoe", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        return html.Div([
                            html.P(data.get("mensaje", "LCOE calculado correctamente")),
                        html.P(f"LCOE: {data.get('lcoe')} {data.get('unidad')}")
                        ]), False
                    else:
                        return f"Error: {response.status_code}", True
                except Exception as e:
                    return f"Error al conectar con el backend: {str(e)}", True
        return "Ingresa los datos y presiona 'Calcular LCOE'", False
    
def register_historial_lcoe_callbacks(app):
    @app.callback(
        Output("tabla-lcoe", "children"),
        [Input("url", "pathname")],
    )
    def obtener_historial_lcoe(pathname):
        # Solo se cargará la tabla se estamos en /historial-lcoe
        if pathname == "/historial-lcoe":
            try:
                response = requests.get(url_base + "/lcoe-data")
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        return html.P("No hay registros de LCOE en la base de datos.")
                    
                    # Convirtiendo el json en DataFrame
                    historial_lcoe_df = pd.DataFrame(data)

                    # Construyendo la tabla
                    table_header = [
                        html.Thead(html.Tr([html.Th(col) for col in historial_lcoe_df.columns]))
                    ]
                    table_body = []
                    for _, row in historial_lcoe_df.iterrows():
                        table_body.append(
                        html.Tr([
                            html.Td(row[col]) for col in historial_lcoe_df.columns
                        ])
                    )
                    table = dbc.Table(table_header + [html.Tbody(table_body)],
                                  bordered=True, 
                                  hover=True,
                                  responsive=True)
                    return table
                else:
                    return dbc.Alert("Error al cargar registros LCOE", color="danger")
            except Exception as e:
                return dbc.Alert("Error al conectar con el backend: " + str(e), color="danger")
        # En caso de no encontrar la ruta /historial-lcoe, se devuelve un mensaje
        return html.P("No se encontró la ruta /historial-lcoe")

def register_historial_interes_compuesto_callbacks(app):
    @app.callback(
        Output("tabla-ic", "children"),
        [Input("url", "pathname")]
    )
    def obtener_historial_interes_compuesto(pathname):
        # Solo se cargará la tabla se estamos en /historial-interes-compuesto
        if pathname == "/historial-interes-compuesto":
            try:
                response = requests.get(url_base + "/interes-compuesto-data")
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        return html.P("No hay registros de Interés Compuesto en la base de datos.")
                    
                    # Convirtiendo el json en DataFrame
                    historial_ic_df = pd.DataFrame(data)

                    # Contruyendo la tabla
                    table_header = [
                        html.Thead(html.Tr([html.Th(col) for col in historial_ic_df.columns]))
                    ]
                    table_body = []
                    for _, row in historial_ic_df.iterrows():
                        table_body.append(
                            html.Tr([
                                html.Td(row[col]) for col in historial_ic_df.columns
                            ])
                        )
                    table = dbc.Table(table_header + [html.Tbody(table_body)],
                                      bordered=True,
                                      hover=True,
                                      responsive=True)
                    return table
                else:
                    return dbc.Alert("Error al cargar registros Interés Compuesto", color="danger")
            except Exception as e:
                return dbc.Alert("Error al conectar con el backend: " + str(e), color="danger")
            
        # Si no esta la ruta /historial-interes-compuesto, se devuelve un mensaje
        return html.P("No se encontró la ruta /historial-interes-compuesto")
                        


# Función para registrar todos los callbacks
def register_all_callbacks(app):
    register_conversion_tasa_callbacks(app)
    register_interes_compuesto_callbacks(app)
    register_lcoe_callbacks(app)
    register_historial_lcoe_callbacks(app)
    register_historial_interes_compuesto_callbacks(app)