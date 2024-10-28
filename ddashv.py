import dash
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table

# Cargar los datos desde el archivo de Excel
file_path = "Datafinal.xlsx"
df = pd.read_excel(file_path)

# Coordenadas de latitud y longitud para cada departamento de Colombia
coordinates = {
    'ANTIOQUIA': {'lat': 6.25184, 'lon': -75.56359},
    'ATLANTICO': {'lat': 10.96854, 'lon': -74.78132},
    'SANTANDER': {'lat': 7.11935, 'lon': -73.12274},
    'BOGOTA D.C.': {'lat': 4.60971, 'lon': -74.08175},
    'VALLE': {'lat': 3.45164, 'lon': -76.53199},
    'CAUCA': {'lat': 2.44481, 'lon': -76.61474},
    'CESAR': {'lat': 10.474245, 'lon': -73.243633},
    'BOYACA': {'lat': 5.45451, 'lon': -73.362},
    'CUNDINAMARCA': {'lat': 4.86798, 'lon': -74.03328},
    'RISARALDA': {'lat': 4.81333, 'lon': -75.69456},
    'MAGDALENA': {'lat': 10.39105, 'lon': -74.40566},
    'META': {'lat': 4.15138, 'lon': -73.63797},
    'BOLIVAR': {'lat': 10.391049, 'lon': -75.479426},
    'NORTE DE SANTANDER': {'lat': 7.9463, 'lon': -72.8988},
    'HUILA': {'lat': 2.9273, 'lon': -75.2819},
    'SUCRE': {'lat': 9.30472, 'lon': -75.39778},
    'TOLIMA': {'lat': 4.4389, 'lon': -75.2322},
    'CORDOBA': {'lat': 8.74798, 'lon': -75.88143},
    'NARINO': {'lat': 1.2145, 'lon': -77.2811},
    'LA GUAJIRA': {'lat': 11.54444, 'lon': -72.90722},
    'QUINDIO': {'lat': 4.53389, 'lon': -75.68111},
    'CALDAS': {'lat': 5.07028, 'lon': -75.51361},
    'CAQUETA': {'lat': 0.86986, 'lon': -73.8419},
    'CASANARE': {'lat': 5.75893, 'lon': -71.57239}
}

# Inicializa la aplicación con Font Awesome
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"], suppress_callback_exceptions=True)
server= app.server

# Configura el diseño
app.layout = html.Div([
    # Barra superior
    html.Div(
        style={
            "width": "100%",
            "height": "50px",
            "backgroundColor": "#219ebc",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "zIndex": 1
        }
    ),
    
    # Barra lateral
    html.Div(
        style={
            "width": "190px",
            "height": "100vh",
            "backgroundColor": "#8ecae6",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "paddingTop": "10px",
            "zIndex": 2
        },
        children=[
            html.Img(src="/assets/loggo.png", style={"width": "120px", "marginBottom": "30px"}),  # Logo
            html.Div(style={"marginTop": "100px"}),
            html.Button(html.Div([html.I(className="fas fa-info-circle", style={"marginRight": "10px"}), "Sobre el proyecto"]), id="tab-1-button", n_clicks=0, style={"background": "transparent", "border": "none", "color": "white", "marginBottom": "20px"}),
            html.Button(html.Div([html.I(className="fas fa-chart-line", style={"marginRight": "10px"}), "Indicadores"]), id="tab-2-button", n_clicks=0, style={"background": "transparent", "border": "none", "color": "white", "marginBottom": "20px"}),
            html.Button(html.Div([html.I(className="fas fas fa-th", style={"marginRight": "10px"}), "Dashboard"]), id="tab-3-button", n_clicks=0, style={"background": "transparent", "border": "none", "color": "white", "marginBottom": "20px"}),
            html.Button(html.Div([html.I(className="fas fa-cogs", style={"marginRight": "10px"}), " "]), id="tab-4-button", n_clicks=0, style={"background": "transparent", "border": "none", "color": "white", "marginBottom": "20px"}),
        
        html.Div(  # Añadido para los nombres
                    [
                        html.H4("Kelly Beltran", style={"color": "white", "display": "inline-block", "margin": "0"}),
                        html.H4("Henry Saenz", style={"color": "white", "display": "inline-block", "marginLeft": "20px", "margin": "0"})
                    ],
                    style={
                        "marginTop": "50px",  # Espacio entre los botones y los nombres
                        "textAlign": "center"  # Centrar texto
                    }
                )
        ]
        
    ),
    
    # Contenedor del contenido
    html.Div(
        style={
            "marginLeft": "190px",
            "marginTop": "60px",
            "padding": "20px",
            "backgroundColor": "#f8f9fa",
            "minHeight": "100vh"
        },
        id="content"
    )
])

# Callback para actualizar el contenido y el color del botón
@app.callback(
    [Output("content", "children"),
     Output("tab-1-button", "style"),
     Output("tab-2-button", "style"),
     Output("tab-3-button", "style"),
     Output("tab-4-button", "style")],
    [Input("tab-1-button", "n_clicks"),
     Input("tab-2-button", "n_clicks"),
     Input("tab-3-button", "n_clicks"),
     Input("tab-4-button", "n_clicks")]
)
def display_content(tab1, tab2, tab3, tab4):
    ctx = callback_context
    clicked_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    style_default = {
        "background": "transparent",
        "border": "none",
        "color": "white",
        "marginBottom": "20px",
        "padding": "10px",
    }
    style_selected = {
        "background": "white",
        "border": "none",
        "color": "#219ebc",
        "marginBottom": "20px",
        "padding": "10px",
        "width": "190px"
    }

    if clicked_id == "tab-1-button":
            content = html.Div([
                html.H3("Desempeño Financiero de PYMEs Colombianas", style={"textAlign": "center"}),
                html.Hr(style={"width": "80%", "borderTop": "1px solid #0097b2", "margin": "10px auto"}),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "flex-start",
                        "padding": "20px",
                        "maxWidth": "1200px",
                        "margin": "0 auto",
                        "marginBottom": "10px"
                    },
                    children=[
                        # Cuadro de texto
                        html.Div(
                            style={
                                "padding": "15px",
                                "borderRadius": "5px",
                                "backgroundColor": "#e6f7ff",  # Fondo claro
                                "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                "width": "55%",
                            },
                            children=[
                                html.P("Las PYMEs son fundamentales en la economía colombiana, representando una parte significativa de la actividad productiva."),
                                html.P("Sin embargo, al solicitar préstamos o atraer inversionistas, a menudo se enfrentan a benchmarks sectoriales que se basan en promedios generales, lo que puede llevar a decisiones de inversión sesgadas.")
                            ]
                        ),
                    
                        # Espacio para la imagen
                        html.Div(
                            style={
                                "width": "40%",
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                            children=[
                                html.Img(src="/assets/lol3.png", style={"width": "100%", "maxWidth": "200px"})
                            ]
                        )
                    ]
                ),

                # Subtítulo centrado
                html.Div(
                    style={
                        "textAlign": "center",
                        "marginTop": "20px"
                    },
                    children=[
                        html.H4("Objetivos", style={"marginBottom": "10px"}),
                        # Descripción sin cuadro
                        html.P("Este proyecto busca proporcionar herramientas útiles para la toma de decisiones de inversión y desarrollo en el sector de las PYMEs."),
                    ]
                ),

                # Cuadros para los objetivos específicos
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "marginTop": "20px"
                    },
                    children=[
                        # Cuadro 1
                        html.Div(
                            style={
                                "padding": "15px",
                                "borderRadius": "5px",
                                "backgroundColor": "#cceeff",  # Fondo azul claro
                                "width": "23%",  # Ancho de cada cuadro
                                "textAlign": "center"  # Centrar el contenido
                            },
                            children=[
                                html.H5("Recolección y Preprocesamiento de Datos",style={"fontWeight": "bold", "color": "#1f5375"}),
                                html.P("Compilar y limpiar datos del DANE sobre PYMEs."),
                                html.Img(src="/assets/segunda.png", style={"width": "100%", "maxWidth": "100px", "marginTop": "10px"})  # Imagen para el cuadro 1
                            ]
                        ),

                        # Cuadro 2
                        html.Div(
                            style={
                                "padding": "15px",
                                "borderRadius": "5px",
                                "backgroundColor": "#cceeff",  # Fondo azul claro
                                "width": "23%",
                                "textAlign": "center"  # Centrar el contenido
                            },
                            children=[
                                html.H5("Construcción de Variables de Desempeño Financiero",style={"fontWeight": "bold", "color": "#1f5375"}),
                                html.P("Calcular índices financieros a partir de estados financieros."),
                                html.Img(src="/assets/cuarta.png", style={"width": "100%", "maxWidth": "100px", "marginTop": "10px"})  # Imagen para el cuadro 2
                            ]
                        ),

                        # Cuadro 3
                        html.Div(
                            style={
                                "padding": "15px",
                                "borderRadius": "5px",
                                "backgroundColor": "#cceeff",  # Fondo azul claro
                                "width": "23%",
                                "textAlign": "center"  # Centrar el contenido
                            },
                            children=[
                                html.H5("Exploración de Datos",style={"fontWeight": "bold", "color": "#1f5375"}),
                                html.P("Identificar patrones y definir umbrales."),
                                html.Img(src="/assets/tercero.png", style={"width": "100%", "maxWidth": "100px", "marginTop": "10px"})  # Imagen para el cuadro 3
                            ]
                        ),

                        # Cuadro 4
                        html.Div(
                            style={
                                "padding": "15px",
                                "borderRadius": "5px",
                                "backgroundColor": "#cceeff",  # Fondo azul claro
                                "width": "23%",
                                "textAlign": "center"  # Centrar el contenido
                            },
                            children=[
                                html.H5("Visualización de Datos",style={"fontWeight": "bold", "color": "#1f5375"}),
                                html.P("Utilizar tableros y mapas de calor para establecer benchmarks por región y sector."),
                                html.Img(src="/assets/primero.png", style={"width": "100%", "maxWidth": "100px", "marginTop": "10px"})  # Imagen para el cuadro 4
                            ]
                        )
                    ]
                )
            ])
            tab1_style, tab2_style, tab3_style, tab4_style = style_selected, style_default, style_default, style_default


    elif clicked_id == "tab-2-button":
        content = html.Div([
            html.H3("Indicadores Financieros y Variables", style={"textAlign": "center"}),

            # Thin line under the title
            html.Hr(style={"width": "80%", "borderTop": "1px solid #0097b2", "margin": "10px auto"}),
            
            
            html.Div(
            style={"marginTop": "10px"},
            children=[
                html.H4("Muestra de Datos", style={"color": "#666", "fontWeight": "normal"})
            ]
            ),  
            # Subtitle centered under the line
            html.Div(
                style={ "marginTop": "20px"},
                children=[
                    html.H4("Variables Cualitativas", style={"color": "#666", "fontWeight": "normal"})
                ]
            ),
            html.Div(
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "space-around",
                    "marginTop": "20px"
                },
                children=[
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("NIT", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Número de identificación tributaria")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("Estado", style={"margin": "0"})
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Estado actual")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("Concepto fiscal", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Concepto  Revisor fiscal en su orme")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("Obligacion fiscal", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Está obligada a tener Revisor fiscal?")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("societario", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Tipo de societario")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("Departamento", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Departamento de la dirección del domicilio")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("seccion", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Seccion Código CIIU")
                        )
                    ]
                    ),
                    html.Div(
                    style={
                        "width": "22%",
                        "margin": "10px",
                        "textAlign": "center"
                    },
                    children=[
                        # Header with dark blue background
                        html.Div(
                            style={
                                "backgroundColor": "#219ebc",
                                "padding": "10px",
                                "borderRadius": "5px 5px 0 0",
                                "color": "white"
                            },
                            children=html.H5("Código", style={"margin": "0"})
                        ),
                        # Description with a different background
                        html.Div(
                            style={
                                "backgroundColor": "#cceeff",
                                "padding": "10px",
                                "borderRadius": "0 0 5px 5px"
                            },
                            children=html.P("Clasificación Industrial Internacional Uniforme Versión 4 A.C (CIIU)")
                        )
                    ]
                    ),
                ]
            ),
            html.Div(
            style={"marginTop": "20px"},
            children=[
                html.H4("Variables Númerica e Indicadores Utilizados", style={"color": "#666", "fontWeight": "normal"})
            ]
            ),

        # Large rectangle containing two columns with variable blocks
        html.Div(
            style={
                "width": "100%", 
                "height": "600px", 
                "backgroundColor": "#e0f7fa", 
                "borderRadius": "10px", 
                "marginTop": "20px", 
                "display": "flex", 
                "padding": "20px",
                "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.2)"
            },
            children=[
                # Left Column
                html.Div(
                    style={"width": "50%", "paddingRight": "10px"},
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Razón corriente"  # Replace with variable name
                                ),
                                html.P("Proporción entre los activos corrientes y los pasivos corrientes.", style={"marginLeft": "10px"})
                            ]
                        ),
                        # Repeat the above html.Div structure for other variables in the left column
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Rotacion inventario"  # Replace with variable name
                                ),
                                html.P("Indica cuántas veces el inventario de productos se vende o utiliza.", style={"marginLeft": "10px"})
                            ]
                        ),
                        # Repeat for Var 3 to Var 6
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Rotación cartera"  # Replace with variable name
                                ),
                                html.P("Calcula el número de veces que la empresa recupera sus cuentas por cobrar.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Rotación proveedores"  # Replace with variable name
                                ),
                                html.P("Indica la frecuencia con la que la empresa paga a proveedores.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Productividad KTNO"  # Replace with variable name
                                ),
                                html.P("Relación entre las ventas o ingresos operativos y el KTNO.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Tasa de Desempleo"  # Replace with variable name
                                ),
                                html.P("Porcentaje de personas en capacidad de trabajar que no tienen empleo pero buscan.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Tasa de Ocupación"  # Replace with variable name
                                ),
                                html.P("Porcentaje de personas en capacidad de trabajar que están empleadas.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="PIB"  # Replace with variable name
                                ),
                                html.P("Valor total de los bienes y servicios producidos dentro del país durante un período específico.", style={"marginLeft": "10px"})
                            ]
                        ),
                        
                    ]
                ),
                # Right Column
                html.Div(
                    style={"width": "50%", "paddingLeft": "10px"},
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "5px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="ROA"  # Replace with variable name
                                ),
                                html.P("Retorno sobre los activos, o rentabilidad de los activos.", style={"marginLeft": "10px"})
                            ]
                        ),
                        # Repeat the above html.Div structure for other variables in the right column
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="ROE"  # Replace with variable name
                                ),
                                html.P("Retorno sobre el patrimonio, o rentabilidad del capital propio.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Nivel de endeudamiento"  # Replace with variable name
                                ),
                                html.P("Proporción de los pasivos sobre los activos totales.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Generación Efectivo"  # Replace with variable name
                                ),
                                html.P("Mide la cantidad de efectivo a partir de operaciones principales.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="FLC"  # Replace with variable name
                                ),
                                html.P("Indica el efectivo disponible después de cubrir todas las operaciones y necesidades de inversión.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="FDC"  # Replace with variable name
                                ),
                                html.P("Indica el efectivo disponible después de cumplir con todos los gastos e inversiones esenciales.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="FDC/FLC"  # Replace with variable name
                                ),
                                html.P("Indicadores de liquidez y estabilidad financiera.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Generación FLC"  # Replace with variable name
                                ),
                                html.P("Indica el efectivo disponible después de cubrir los gastos operativos y de capital.", style={"marginLeft": "10px"})
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                            children=[
                                html.Div(
                                    style={
                                        "width": "200px", "height": "40px", 
                                        "backgroundColor": "#219ebc", "borderRadius": "3px",
                                        "color": "white", "display": "flex", "alignItems": "center",
                                        "justifyContent": "center", "fontWeight": "bold"
                                    },
                                    children="Cantidad de años"  # Replace with variable name
                                ),
                                html.P("Cantidad de años que tiene la empresa.", style={"marginLeft": "10px"})
                            ]
                        )
                    ]
                )
            ]
        )

        ])

        tab1_style, tab2_style, tab3_style, tab4_style = style_default, style_selected, style_default, style_default
    elif clicked_id == "tab-3-button":
        # Contenido del Dashboard de código 2
        content = html.Div([
            html.H3("Dashboard"),
            html.P("Selecciona las opciones para filtrar los gráficos del dashboard."),
            
            # Filtros
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in df['Fecha de Corte'].unique()],
                    placeholder='Seleccione Año',
                    style={'width': '40%'}
                ),
                dcc.Dropdown(
                    id='dept-dropdown',
                    options=[{'label': dept, 'value': dept} for dept in df['Departamento de la dirección del domicilio'].unique()],
                    placeholder='Seleccione Departamento',
                    style={'width': '40%'}
                ),
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[{'label': type_soc, 'value': type_soc} for type_soc in df['Tipo societario'].unique()],
                    placeholder='Seleccione Tipo de Empresa',
                    style={'width': '40%'}
                ),
            ], style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'marginBottom': '20px'
            }),
            
            # Gráficos
            dcc.Graph(id='department-bar-chart'),
            html.Div([
                dcc.Graph(id='pib-bar-chart', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='occupation-bar-chart', style={'width': '48%', 'display': 'inline-block'})
            ]),
            html.Div([
                dcc.Graph(id='pib-bubble-map', style={'width': '48%', 'display': 'inline-block'}),
                html.Div(id='top-8-pib-table', style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ]),
            html.Div([
                dcc.Graph(id='fdc-violin-plot', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='flc-violin-plot', style={'width': '48%', 'display': 'inline-block'})
            ])
        ])
        tab1_style, tab2_style, tab3_style, tab4_style = style_default, style_default, style_selected, style_default
    else:
        content = html.H3("Selecciona una pestaña")
        tab1_style, tab2_style, tab3_style, tab4_style = style_default, style_default, style_default, style_default

    return content, tab1_style, tab2_style, tab3_style, tab4_style

# Callback para actualizar los gráficos
@app.callback(
    [Output('department-bar-chart', 'figure'),
     Output('pib-bar-chart', 'figure'),
     Output('occupation-bar-chart', 'figure'),
     Output('pib-bubble-map', 'figure'),
     Output('top-8-pib-table', 'children'),
     Output('fdc-violin-plot', 'figure'),
     Output('flc-violin-plot', 'figure')],
    [Input('year-dropdown', 'value'),
     Input('dept-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_dashboard(year, dept, type_soc):
    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['Fecha de Corte'] == year]
    if dept:
        filtered_df = filtered_df[filtered_df['Departamento de la dirección del domicilio'] == dept]
    if type_soc:
        filtered_df = filtered_df[filtered_df['Tipo societario'] == type_soc]
    
    dept_counts = df['Departamento de la dirección del domicilio'].value_counts().nlargest(10)
    fig_department = px.bar(dept_counts, x=dept_counts.index, y=dept_counts.values, title='Conteo de Empresas por Departamento', labels={'x': 'Departamento', 'y': 'Cantidad de Empresas'})
    
    total_pib = filtered_df.groupby('Clasificación Industrial Internacional Uniforme Versión 4 A.C (CIIU)')['PIB'].sum().nlargest(5)
    fig_pib = px.bar(total_pib, x=total_pib.index.str[:5] + '...', y=total_pib.values, title='Top 5 Contribuciones al PIB por Sectores', labels={'x': 'Sector', 'y': 'PIB'})
    
    occupation = filtered_df.groupby('Clasificación Industrial Internacional Uniforme Versión 4 A.C (CIIU)')['Tasa de Ocupación'].mean().nlargest(5)
    fig_occupation = px.bar(occupation, x=occupation.index.str[:5] + '...', y=occupation.values, title='Top 5 Sectores con Mayor Tasa de Ocupación', labels={'x': 'Sector', 'y': 'Tasa de Ocupación'})
    
    df_geo = df.copy()
    df_geo['lat'] = df_geo['Departamento de la dirección del domicilio'].apply(lambda x: coordinates.get(x, {}).get('lat', None))
    df_geo['lon'] = df_geo['Departamento de la dirección del domicilio'].apply(lambda x: coordinates.get(x, {}).get('lon', None))
    df_geo = df_geo.dropna(subset=['lat', 'lon'])
    fig_pib_bubble = px.scatter_geo(df_geo, lat='lat', lon='lon', size='PIB DEP', color='Departamento de la dirección del domicilio', title='PIB por Departamento', labels={'size': 'PIB DEP'}, hover_name='Departamento de la dirección del domicilio', size_max=60, projection='mercator')
    
    top_8_pib = df.groupby('Departamento de la dirección del domicilio')['PIB DEP'].sum().nlargest(8).reset_index()
    table_rows = [html.Tr([html.Td(row['Departamento de la dirección del domicilio']), html.Td(f"{row['PIB DEP']:.2f}")]) for index, row in top_8_pib.iterrows()]
    table = dbc.Table([html.Thead(html.Tr([html.Th('Departamento'), html.Th('PIB DEP')]))] + [html.Tbody(table_rows)], bordered=True, hover=True, responsive=True, striped=True)
    
    fig_fdc_violin = px.violin(filtered_df, x='FDC', box=True, points="all", title="Distribución de FDC")
    fig_flc_violin = px.violin(filtered_df, x='FLC', box=True, points="all", title="Distribución de FLC")
    
    return fig_department, fig_pib, fig_occupation, fig_pib_bubble, table, fig_fdc_violin, fig_flc_violin

# Ejecuta la aplicación
if __name__ == "__main__":
    app.run_server()
