import dash
import requests
import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Definiendo la URL de la API
url_base = "http://10.253.13.90:8000"

# ------------------------------------------------------------------------------
# Layouts
# ------------------------------------------------------------------------------

def get_inicio_layout():
    return dbc.Container([
        # Título principal
        html.H1("Calculadora Financiera", style={"textAlign": "center", "fontSize": "3em", "marginBottom": "10px", "color": "#343a40"}),
        html.P("Nos alegra tenerte aquí. Esta herramienta te permitirá estimar, comparar y planificar diferentes escenarios de inversión y costos energéticos de manera rápida y sencilla. Selecciona una de las opciones del menú para comenzar.", style={"color": "#6c757d", "fontSize": "1.2em", "textAlign": "justify", "marginBottom": "40px"}),
        html.Hr(style={"borderColor": "#dee2e6", "margin": "0 auto", "width": "50%"}),

        # Sección de descripción
        html.Div([
            html.H2("¿Qué es esta herramienta?", style={"color": "#495057", "fontSize": "1.5em", "textAlign": "center", "marginTop": "30px"}),
            html.P("Nuestra aplicación te ayuda a estimar costos energéticos (LCOE), calcular interés compuesto y convertir tasas de interés, de manera rápida y precisa.", style={"color": "#6c757d", "fontSize": "1.2em", "textAlign": "justify", "marginBottom": "40px"})
        ]),

        # Sección de llamada a la acción
        html.Div([
            html.H3("Empieza ahora", style={"color": "#495057", "fontSize": "1.3em", "textAlign": "center", "marginTop": "30px"}),
            html.P("Da el primer paso hacia tu futuro financiero: elige una opción y comienza a calcular.", style={"color": "#6c757d", "fontSize": "1.1em", "textAlign": "justify"}),
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Calcular LCOE", color="primary", href="/lcoe"), width="auto"),
                    dbc.Col(dbc.Button("Interés Compuesto", color="success", href="/interes-compuesto"), width="auto"),
                    dbc.Col(dbc.Button("Convertir Tasas", color="info", href="/conversion-tasa"), width="auto"),
                ],
                justify="center",
                className="mt-3"
            )
        ])
    ], fluid=True, style={"padding": "40px 20px", "backgroundColor": "#f8f9fa", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"})

def get_lcoe_layout():
    return dbc.Container([
    html.Div([
        html.H1("Cálculo de LCOE", style={"textAlign": "center", "fontSize": "2.5em", "color": "#343a40"}),
        html.P("Ingresa los datos para calcular el costo nivelado de energía para tu proyecto.", style={"textAlign": "center", "fontSize": "1.2em", "color": "#6c757d", "marginBottom": "20px"}),
        html.Hr(),

    # Formulario con grid responsivo
    dbc.Form([
        dbc.Row([
            dbc.Col([
                html.Label("CAPEX: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-capex", type="number", value=0, className="form-control", style={"borderRadius": "5px"}),
                dbc.Tooltip("Incluye costos de adquisición de terrenos, equipos, construcción, ingeniería y otros gastos relacionados con la puesta en marcha del proyecto.", target="input-capex"),
            ], md=6),
            dbc.Col([
                html.Label("OPEX: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-opex", type="number", value=0, className="form-control", style={"borderRadius": "5px"}),
                dbc.Tooltip("Incluye costos de combustible, personal, mantenimiento, seguros, impuestos y otros gastos recurrentes.", target="input-opex"),
            ], md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Producción anual (MWh): ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-annual-production", type="number", value=0, className="form-control", style={"borderRadius": "5px"}),
                dbc.Tooltip("Es la cantidad de energía eléctrica que la planta genera en un año, medida en megavatios hora.", target="input-annual-production"),
            ], md=6),
            dbc.Col([
                html.Label("Tasa de descuento: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-discount-rate", type="number", value=0, className="form-control", style={"borderRadius": "5px"}),
                dbc.Tooltip("Representa el costo de oportunidad del capital y refleja el riesgo del proyecto.", target="input-discount-rate"),
            ], md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Plazo de vida de la planta en años: ", style={"fontWeight": "bold", "fontSize": "1.1em"}),
                dcc.Input(id="input-project-life", type="number", value=0, className="form-control", style={"borderRadius": "5px"}),
                dbc.Tooltip("Es el período de tiempo durante el cual se espera que la planta genere energía de manera eficiente.", target="input-project-life"),
            ], md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                # Boton para calcular el lcoe
                dbc.Button([html.I(className="fas fa-calculator"), "Calcular LCOE"], id="button-lcoe", n_clicks = 0, size="lg", color="outline-primary", className="mt-3 me-3"),
                # Boton para limpiar todos los campos
                dbc.Button([html.I(className="fas fa-calculator"), "Reiniciar"], id = "button-reset-lcoe", n_clicks = 0, size="lg", color="outline-secondary", className="mt-3"),
            ], md=12),
        ], className="mb-4"),
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
    ], style={"backgroundColor": "#f1f3f5", "padding": "15px", "borderRadius": "5px", "marginBottom": "20px"})
], fluid=True, className="d-flex justify-content-center")

def get_interes_compuesto_layout():
    return dbc.Container([
        html.Div([
            # Sección de encabezado
            html.H1("Cálculo de Interés Compuesto", style={"textAlign": "center", "fontSize": "2.5em", "marginBottom": "20px", "color": "#343a40"}),
            html.P("Calcula el valor futuro de tu inversión.", style={"textAlign": "center", "fontSize": "1.2em", "color": "#6c757d", "marginBottom": "30px"}),
            html.Hr(),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        html.Label("Capital inicial: ", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                        dcc.Input(id = "input-capital", type = "number", value=0, className="form-control", style={"borderRadius": "5px"}),
                        dbc.Tooltip("Es la cantidad de dinero que inviertes o depositas al principio.",target = "input-capital"),
                    ], md = 6),

                    dbc.Col([
                        html.Label("Tasa de interés: ", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                        dcc.Input(id = "input-tasa-interes", type = "number", value=0, className="form-control", style={"borderRadius": "5px"}),
                        dbc.Tooltip("Es el porcentaje que te pagan por tu dinero durante un período de tiempo.",target = "input-tasa-interes"),
                    ], md = 6),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Plazo en periodos (años o meses o días): ", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                        dcc.Input(id = "input-plazo", type = "number", value=0, className="form-control", style={"borderRadius": "5px"}),
                        dbc.Tooltip("Es el tiempo que dejas tu dinero invertido.",target = "input-plazo"),
                    ], md = 6),

                    dbc.Col([
                        html.Label("Tipo de tasa (diaria, mensual o anual)", className="form-label", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                        dcc.Dropdown(
                            id = "dropdown-interes-compuesto", 
                            options = [
                                {"label": "ANUAL", "value": "anual"},
                                {"label": "MENSUAL", "value": "mensual"},
                                {"label": "DIARIO", "value": "diario"}
                            ],
                        placeholder = "Selecciona el tipo de tasa",
                        className="custom-dropdown",  # You can define custom CSS
                        style={
                            'width': '100%',
                            'border-radius': '0.25rem',
                            'border': '1px solid #ced4da'
                        }
                        ),
                        dbc.Tooltip("Indica con qué frecuencia se añade el interés a tu capital, y esto afecta a la rapidez con la que crece tu dinero.",target = "dropdown-interes-compuesto"),
                    ], md = 6, className="form-group"),
                ], className = "mb-4"),

                dbc.Row([
                    dbc.Col([
                        dbc.Button([html.I(className="fas fa-calculator"), "Calcular"], id="button-interes-compuesto", n_clicks = 0, size="lg", color="outline-primary", className="mt-3 me-3"),
                        dbc.Button([html.I(className="fas fa-calculator"), "Reiniciar"], id = "button-reset-ic", n_clicks = 0, size="lg", color="outline-secondary", className="mt-3"),
                    ], md = 12)
                ], className="mb-4"),
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
            html.H1("Conversor de Tasas de Interés", style={"textAlign": "center", "fontSize": "2.5em", "color": "#343a40"}),
            html.P("Convierte entre diferentes tipos de tasas de interés.", style={"textAlign": "center", "fontSize": "1.2em", "color": "#6c757d", "marginBottom": "20px"}),
            html.Hr(),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Tasa (%)", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                    dcc.Input(id = "input-tasa", type = "number", placeholder = "Ingresa la tasa", debounce = True, className="form-control", style={"borderRadius": "5px"}),
                    dbc.Tooltip("""Representa el "precio" del dinero, es decir, lo que se paga por usarlo (si pides un préstamo) o lo que se gana por prestarlo o invertirlo (si tienes un depósito o inversión).""",target = "input-tasa"),
                ],md = 6),
                dbc.Col([
                    html.Label("Tipo de tasa", style={"fontWeight": "bold", "fontSize": "1.1em", "color": "#343a40"}),
                    dcc.Dropdown(
                        id="dropdown",
                        options=[
                            {"label": "ANUAL", "value": "anual"},
                            {"label": "MENSUAL", "value": "mensual"},
                            {"label": "DIARIO", "value": "diario"}
                        ],
                        placeholder="Selecciona el tipo de tasa",
                        className = "custom-dropdown", 
                        style={
                            'width': '100%',
                            "borderRadius": "5px",
                            'border': '1px solid #ced4da'
                        }
                    ),
                    dbc.Tooltip("Se refiere a la frecuencia con la que se calcula y aplica el interés a tu capital.",target = "dropdown"),
                ],md = 6, className="form-group")
            ], className = "mb-4"),

            dbc.Row([
                dbc.Col([
                    dbc.Button([html.I(className="fas fa-calculator"), "Convierte"], id="btn-convertir", n_clicks=0, size="lg", color="outline-primary", className="mt-3 me-3"),
                    dbc.Button([html.I(className="fas fa-undo"), "Reiniciar"], id = "button-reset-ct", n_clicks = 0, size="lg", color="outline-secondary", className="mt-3"),
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
        [Output("output-ct", "children"),
         Output("error-alert-ct", "is_open"),
         Output("input-tasa", "value"),
         Output("dropdown", "value")],
        [Input("btn-convertir", "n_clicks"),
         Input("button-reset-ct", "n_clicks")],
        [State("input-tasa", "value"),
         State("dropdown", "value")]
    )
    def convertir_tasas(calc_clicks, reset_clicks, tasa, tipo):
        # Si no se ha clicado ningún botón, devolver estado inicial
        ctx = dash.callback_context
        if not ctx.triggered:
            return ["Ingrese los datos y presiona 'Calcular'", False, 0, None]
        
        # Identigicar qué botón fue clicado
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "btn-convertir" and calc_clicks > 0:
            calc_clicks = 0
            if tasa is None or tipo is None:
                return ["Ingrese los datos y presiona 'Calcular'", True, tasa, tipo]
            else:
                # Se prepara el payload para la llamada a la API (según el modelo)
                payload = {"tasa": float(tasa), "tipo": tipo}

                try:
                    # Se llama a la API
                    response = requests.post(url_base + "/convertir-tasas", json = payload)
                    
                    # Se procesa la respuesta
                    if response.status_code == 200:
                        data = response.json()
                        print(data)
                        return [html.Div([
                            html.P(data.get("mensaje", "Conversión exitosa")),
                            html.P(f"Tasa Diaria: {data.get('tasa_diaria')}%"),
                            html.P(f"Tasa Mensual: {data.get('tasa_mensual')}%"),
                            html.P(f"Tasa Anual: {data.get('tasa_anual')}%")
                        ]), False, tasa, tipo
                        ]
                    else:
                        return f"Error: {response.status_code}"
                except Exception as e:
                    return f"Error al conectar con el backend: {str(e)}"
        elif button_id == "button-reset-ct" and reset_clicks > 0:
            return ["Ingresa los datos y presiona 'convertir'", False, 0, None]
    
def register_interes_compuesto_callbacks(app):
    @app.callback(
        [Output("output-interes-compuesto", "children"),
         Output("error-alert-ic", "is_open"),
         Output("input-capital", "value"),
         Output("input-tasa-interes", "value"),
         Output("input-plazo", "value"),
         Output("dropdown-interes-compuesto", "value")],
        [Input("button-interes-compuesto", "n_clicks"), 
         Input("button-reset-ic", "n_clicks")],
        [State("input-capital", "value"),
         State("input-tasa-interes", "value"),
         State("input-plazo", "value"),
         State("dropdown-interes-compuesto", "value")]
    )
    def calcular_interes_compuesto(calc_clicks, reset_clicks, capital, tasa, plazo, tipo):
        # Estado inicial cuando no se ha clicado ningún botón
        ctx = dash.callback_context
        if not ctx.triggered:
            return ["Ingrese los datos y presiona 'Calcular'", False, 0, 0, 0, None]
        
        # Identificar el botón clicado
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Lógica para el botón de cálculo
        if button_id == "button-interes-compuesto" and calc_clicks > 0:
            if None in [capital, tasa, plazo, tipo] or any(x == 0 for x in [capital, tasa, plazo]):
                return ["Ingresa todos los datos correctamente", True, capital, tasa, plazo, tipo]
            else:
                # Preparar el payload para la API
                payload = {
                    "capital": float(capital),
                    "tasa": float(tasa),
                    "plazo": float(plazo),
                    "tipo_tasa": tipo
                }
                try:
                    # Llamada a la API
                    response = requests.post(url_base + "/interes-compuesto", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        return [html.Div([
                            html.P(f"Capital Inicial: {data.get('capital_inicial')}"),
                            html.P(f"Tasa Aplicada: {data.get('tasa_aplicada')}"),
                            html.P(f"Tasa Anual Equivalente: {data.get('tasa_anual_equivalente')}"),
                            html.P(f"Plazo: {data.get('plazo')}"),
                            html.P(f"Monto final: {data.get('monto_final')}"),
                            html.P(f"Ganancias: {data.get('ganancias')}"),
                        ]), False, capital, tasa, plazo, tipo]
                    else:
                        return [f"Error: {response.status_code}", True, capital, tasa, plazo, tipo]
                except Exception as e:
                    return [f"Error al conectar con el backend: {str(e)}", True, capital, tasa, plazo, tipo]
        
        # Lógica para el botón de reset
        elif button_id == "button-reset-ic" and reset_clicks > 0:
            return ["Ingresa los datos y presiona 'Calcular'", False, 0, 0, 0, None]
        
        # Si no se cumple ninguna condición, no actualizar
        return dash.no_update

def register_lcoe_callbacks(app):
    @app.callback(
        [Output("output-lcoe", "children"),
         Output("error-alert-lcoe", "is_open"),
         Output("input-capex", "value"),
         Output("input-opex", "value"),
         Output("input-annual-production", "value"),
         Output("input-discount-rate", "value"),
         Output("input-project-life", "value")],

        [Input("button-lcoe", "n_clicks"),
         Input("button-reset-lcoe", "n_clicks")],

        [State("input-capex", "value"),
         State("input-opex", "value"),
         State("input-annual-production", "value"),
         State("input-discount-rate", "value"),
         State("input-project-life", "value")]
    )
    def handle_lcoe_actions(calc_clicks, reset_clicks, capex, opex, annual_production, discount_rate, project_life):
        # Si no se ha clicado ningún botón, devolver estado inicial
        ctx = dash.callback_context
        if not ctx.triggered:
            return ["Ingresa los datos y presiona 'Calcular LCOE'", False, 0, 0, 0, 0, 0]

        # Identificar qué botón fue clicado
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Lógica para el botón de cálculo
        if button_id == "button-lcoe" and calc_clicks > 0:
            if None in [capex, opex, annual_production, discount_rate, project_life] or any(x == 0 for x in [capex, opex, annual_production, discount_rate, project_life]):
                return ["Ingresa los datos y presiona 'Calcular LCOE'", True, capex, opex, annual_production, discount_rate, project_life]
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
                        return [html.Div([
                            html.P(data.get("mensaje", "LCOE calculado correctamente")),
                            html.P(f"LCOE: {data.get('lcoe')} {data.get('unidad')}")
                        ]), False, capex, opex, annual_production, discount_rate, project_life]
                    else:
                        return [f"Error: {response.status_code}", True, capex, opex, annual_production, discount_rate, project_life]
                except Exception as e:
                    return [f"Error al conectar con el backend: {str(e)}", True, capex, opex, annual_production, discount_rate, project_life]

        # Lógica para el botón de reset
        elif button_id == "button-reset-lcoe" and reset_clicks > 0:
            return ["Ingresa los datos y presiona 'Calcular LCOE'", False, 0, 0, 0, 0, 0]

        # Si no se cumple ninguna condición, no actualizar
        return dash.no_update
    
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
                    
                    table = dash_table.DataTable(
                        # table_header + [html.Tbody(table_body)],
                        id="historial-lcoe-table",
                        columns= [ # {"name": i, "id": i} for i in historial_lcoe_df.columns],
                            {'name': 'Producción anual', 'id': 'produccion_anual'},
                            # {'name': 'id', 'id': 'id'},
                            {'name': 'Vida util', 'id': 'vida_util'},
                            {'name': 'OPEX', 'id': 'opex'},
                            {'name': 'CAPEX', 'id': 'capex'},
                            {'name': 'Tasa de descuento', 'id': 'tasa_descuento'},
                            {'name': 'LCOE', 'id': 'lcoe'},
                        ],
                        data= historial_lcoe_df.to_dict("records"),
                        editable=True,
                        row_deletable=True,
                    )
                    return table
                else:
                    return dbc.Alert("Error al cargar registros LCOE", color="danger")
            except Exception as e:
                return dbc.Alert("Error al conectar con el backend: " + str(e), color="danger")
        # En caso de no encontrar la ruta /historial-lcoe, se devuelve un mensaje
        return html.P("No se encontró la ruta /historial-lcoe")

def update_database_lcoe(app):
    @app.callback(
        Output("historial-lcoe-table", "data"),
        [Input("historial-lcoe-table", "data_previous")],
        [State("historial-lcoe-table", "data")],
        prevent_initial_call=True,
    )
    def update_database_lcoe(data_previous, data):
        if data_previous is not None and data is not None:
            # Se obtiene la diferencia entre los dos conjuntos de datos
            diff = [x for x in data if x not in data_previous]
            # Si hay diferencias, se envía la información al backend
            if diff:
                # Se envía la información al backend por medio de una solicitud PUT
                # se extrae el id del cambio
                id = diff[0]['id']
                json_database_lcoe = diff[0]
                del(json_database_lcoe['id'])
                del(json_database_lcoe['lcoe'])
                # pasar la solicitud PUT
                response = requests.put(url_base + f"/lcoe/{id}", json=json_database_lcoe)
                if response.status_code == 200:
                    # obtener data actualizada
                    response = requests.get(url_base + "/lcoe-data")
                    data = response.json()
                    historial_lcoe_df = pd.DataFrame(data)
                    data= historial_lcoe_df.to_dict("records")
                    return data
                else:
                    return data_previous
            else:
                # encontrar si se ha eliminado una fila
                size_previous = len(data_previous)
                size_current = len(data)
                if size_previous > size_current:
                    # se extrae el id del cambio
                    # Listar los id de los elementos
                    id_previous = [x['id'] for x in data_previous]
                    id_current = [x['id'] for x in data]
                    id = [x for x in id_previous if x not in id_current][0]
                    response = requests.delete(url_base + f"/lcoe/{id}")
                    if response.status_code == 200:
                        # obtener data actualizada
                        response = requests.get(url_base + "/lcoe-data")
                        data = response.json()
                        historial_lcoe_df = pd.DataFrame(data)
                        data= historial_lcoe_df.to_dict("records")
                        return data
                    else:
                        return data_previous
                return data_previous
        else:
            return data_previous

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
                    # table_header = [
                    #     html.Thead(html.Tr([html.Th(col) for col in historial_ic_df.columns]))
                    # ]
                    # table_body = []
                    # for _, row in historial_ic_df.iterrows():
                    #     table_body.append(
                    #         html.Tr([
                    #             html.Td(row[col]) for col in historial_ic_df.columns
                    #         ])
                    #     )
                    table = dash_table.DataTable(
                        id="historial-ic-table",
                        columns= [ # {"name": i, "id": i} for i in historial_ic_df.columns],
                            {'name': 'Capital inicial', 'id': 'capital'},
                            {'name': 'Plazo', 'id': 'plazo'},
                            {'name': 'Tasa de interés', 'id': 'tasa'},
                            {'name': 'Monto final', 'id': 'monto_final'},
                            {'name': 'Ganancias', 'id': 'ganancias'}
                        ],
                        data= historial_ic_df.to_dict("records"),
                        editable=True,
                        row_deletable=True,
                    )
                    # table = dbc.Table(table_header + [html.Tbody(table_body)],
                    #                   bordered=True,
                    #                   hover=True,
                    #                   responsive=True,
                    #                   className="text-center")
                    return table
                else:
                    return dbc.Alert("Error al cargar registros Interés Compuesto", color="danger")
            except Exception as e:
                return dbc.Alert("Error al conectar con el backend: " + str(e), color="danger")
            
        # Si no esta la ruta /historial-interes-compuesto, se devuelve un mensaje
        return html.P("No se encontró la ruta /historial-interes-compuesto")        

def update_database_interes_compuesto(app):
    @app.callback(
        Output("historial-ic-table", "data"),
        [Input("historial-ic-table", "data_previous")],
        [State("historial-ic-table", "data")],
        prevent_initial_call=True,
    )
    def update_database_ic(data_previous, data):
        if data_previous is not None and data is not None:
            # Se obtiene la diferencia entre los dos conjuntos de datos
            diff = [x for x in data if x not in data_previous]
            # Si hay diferencias, se envía la información al backend
            if diff:
                # Se envía la información al backend por medio de una solicitud PUT
                # se extrae el id del cambio
                id = diff[0]['id']
                json_database_ic = diff[0]
                del(json_database_ic['id'])
                del(json_database_ic['monto_final'])
                del(json_database_ic['ganancias'])
                json_database_ic['tipo_tasa'] = 'anual'
                # pasar la solicitud PUT
                response = requests.put(url_base + f"/interes-compuesto/{id}", json=json_database_ic)
                if response.status_code == 200:
                    # obtener data actualizada
                    response = requests.get(url_base + "/interes-compuesto-data")
                    data = response.json()
                    historial_ic_df = pd.DataFrame(data)
                    data= historial_ic_df.to_dict("records")
                    return data
                else:
                    return data_previous
            else:
                # encontrar si se ha eliminado una fila
                size_previous = len(data_previous)
                size_current = len(data)
                if size_previous > size_current:
                    # se extrae el id del cambio
                    # Listar los id de los elementos
                    id_previous = [x['id'] for x in data_previous]
                    id_current = [x['id'] for x in data]
                    id = [x for x in id_previous if x not in id_current][0]
                    response = requests.delete(url_base + f"/interes-compuesto/{id}")
                    if response.status_code == 200:
                        # obtener data actualizada
                        response = requests.get(url_base + "/interes-compuesto-data")
                        data = response.json()
                        historial_ic_df = pd.DataFrame(data)
                        data= historial_ic_df.to_dict("records")
                        return data
                    else:
                        return data_previous
                return data_previous
        else:
            return data_previous

                


# Función para registrar todos los callbacks
def register_all_callbacks(app):
    register_conversion_tasa_callbacks(app)
    register_interes_compuesto_callbacks(app)
    register_lcoe_callbacks(app)
    register_historial_lcoe_callbacks(app)
    register_historial_interes_compuesto_callbacks(app)
    update_database_lcoe(app)
    update_database_interes_compuesto(app)
