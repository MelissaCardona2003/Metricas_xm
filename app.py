import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import sys
import os
from io import BytesIO
import base64

# Agregar el path de la API_XM al sistema
sys.path.append('/home/melissa/Documentos/dashboard-energia-xm/API_XM')
from pydataxm.pydataxm import ReadDB

import warnings
warnings.filterwarnings("ignore")

# Inicializar la aplicación Dash con tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app.title = "Dashboard Energético XM - Colombia"

# Exponer el servidor Flask para producción
server = app.server

# Inicializar API XM
try:
    objetoAPI = ReadDB()
    todas_las_metricas = objetoAPI.get_collections()
    print("API XM inicializada correctamente")
    print(f"Métricas disponibles: {len(todas_las_metricas)}")
except Exception as e:
    print(f"Error al inicializar API XM: {e}")
    todas_las_metricas = pd.DataFrame()

# Función para obtener opciones únicas de MetricId y Entity
def get_metric_options():
    if todas_las_metricas.empty:
        return [], []
    
    # Crear opciones de métricas y ordenarlas alfabéticamente por MetricName
    metric_options = [
        {"label": f"{row['MetricId']} - {row['MetricName']}", "value": row['MetricId']}
        for _, row in todas_las_metricas.iterrows()
    ]
    
    # Ordenar alfabéticamente por el label (que incluye MetricName)
    metric_options = sorted(metric_options, key=lambda x: x['label'])
    
    entity_options = [
        {"label": entity, "value": entity}
        for entity in todas_las_metricas['Entity'].unique()
        if pd.notna(entity)
    ]
    
    # También ordenar las entidades alfabéticamente
    entity_options = sorted(entity_options, key=lambda x: x['label'])
    
    return metric_options, entity_options

metric_options, entity_options = get_metric_options()

# Layout de la aplicación
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="bi bi-lightning-charge-fill me-3"),
                    "Dashboard Energético XM"
                ], className="text-center mb-0 text-primary"),
                html.P("Sistema de Información del Mercado Eléctrico Mayorista - Colombia", 
                       className="text-center text-muted")
            ], className="py-4")
        ])
    ]),
    
    # Controles principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="bi bi-sliders me-2"),
                        "Controles de Consulta"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Métrica:", className="fw-bold"),
                            dcc.Dropdown(
                                id="metric-dropdown",
                                options=metric_options,
                                value=metric_options[0]["value"] if metric_options else None,
                                placeholder="Selecciona una métrica...",
                                className="mb-3"
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Entidad:", className="fw-bold"),
                            dcc.Dropdown(
                                id="entity-dropdown",
                                options=entity_options,
                                value=entity_options[0]["value"] if entity_options else None,
                                placeholder="Primero selecciona una métrica...",
                                className="mb-3"
                            )
                        ], md=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Fecha Inicio:", className="fw-bold"),
                            dcc.DatePickerSingle(
                                id="start-date",
                                date=date.today() - timedelta(days=30),
                                display_format="YYYY-MM-DD",
                                className="mb-3"
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Fecha Fin:", className="fw-bold"),
                            dcc.DatePickerSingle(
                                id="end-date",
                                date=date.today(),
                                display_format="YYYY-MM-DD",
                                className="mb-3"
                            )
                        ], md=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="bi bi-search me-2"), "Consultar Datos"],
                                id="query-button",
                                color="primary",
                                size="lg",
                                className="w-100 mb-2"
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="bi bi-file-earmark-spreadsheet-fill me-2"), "Exportar TODAS las Métricas a Excel"],
                                id="simple-export-button",
                                color="success",
                                size="lg",
                                className="w-100 mb-2"
                            )
                        ], md=6)
                    ])
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),
    
    # Indicadores de estado
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading-indicator",
                children=[html.Div(id="loading-output")],
                type="default"
            )
        ], md=6),
        dbc.Col([
            dcc.Loading(
                id="export-loading-indicator",
                children=[html.Div(id="export-status")],
                type="default"
            )
        ], md=6)
    ], className="mb-3"),
    
    # Información de la métrica seleccionada
    dbc.Row([
        dbc.Col([
            html.Div(id="metric-info")
        ])
    ], className="mb-4"),
    
    # Pestañas para diferentes visualizaciones
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="📊 Tabla de Datos", tab_id="table-tab"),
                dbc.Tab(label="📈 Gráfico de Líneas", tab_id="line-chart-tab"),
                dbc.Tab(label="📊 Gráfico de Barras", tab_id="bar-chart-tab"),
                dbc.Tab(label="📋 Resumen Estadístico", tab_id="stats-tab"),
            ], id="tabs", active_tab="table-tab", className="mb-3")
        ])
    ]),
    
    # Contenido de las pestañas
    dbc.Row([
        dbc.Col([
            html.Div(id="tab-content")
        ])
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                "Desarrollado con ❤️ usando ",
                html.A("Plotly Dash", href="https://dash.plotly.com/", target="_blank"),
                " y la API de ",
                html.A("XM S.A. E.S.P.", href="https://www.xm.com.co/", target="_blank")
            ], className="text-center text-muted small")
        ])
    ], className="mt-5")
    
], fluid=True, className="px-4")

# Callback para actualizar las opciones de entidad según la métrica seleccionada
@app.callback(
    [Output("entity-dropdown", "options"),
     Output("entity-dropdown", "value")],
    [Input("metric-dropdown", "value")]
)
def update_entity_options(selected_metric):
    if not selected_metric or todas_las_metricas.empty:
        return [], None
    
    # Filtrar las entidades disponibles para la métrica seleccionada
    metric_data = todas_las_metricas[todas_las_metricas['MetricId'] == selected_metric]
    
    if metric_data.empty:
        return [], None
    
    # Obtener las entidades únicas para esta métrica
    available_entities = metric_data['Entity'].dropna().unique()
    
    entity_options = [
        {"label": entity, "value": entity}
        for entity in available_entities
    ]
    
    # Ordenar las entidades alfabéticamente
    entity_options = sorted(entity_options, key=lambda x: x['label'])
    
    # Seleccionar automáticamente la primera entidad disponible (después del ordenamiento)
    default_value = entity_options[0]["value"] if len(entity_options) > 0 else None
    
    return entity_options, default_value

# Callback para mostrar información de la métrica seleccionada
@app.callback(
    Output("metric-info", "children"),
    [Input("metric-dropdown", "value")]
)
def display_metric_info(selected_metric):
    if not selected_metric or todas_las_metricas.empty:
        return dbc.Alert("Selecciona una métrica para ver su información.", color="info")
    
    metric_data = todas_las_metricas[todas_las_metricas['MetricId'] == selected_metric]
    
    if metric_data.empty:
        return dbc.Alert("Métrica no encontrada.", color="warning")
    
    # Obtener información de todas las variantes de la métrica
    metric_name = metric_data.iloc[0]['MetricName']
    available_entities = metric_data['Entity'].dropna().unique()
    metric_type = metric_data.iloc[0].get('Type', 'N/A')
    max_days = metric_data.iloc[0].get('MaxDays', 'N/A')
    units = metric_data.iloc[0].get('MetricUnits', 'N/A')
    description = metric_data.iloc[0].get('MetricDescription', 'Sin descripción disponible')
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6([
                html.I(className="bi bi-info-circle me-2"),
                f"Información: {metric_name}"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Strong("ID: "), selected_metric
                ], md=3),
                dbc.Col([
                    html.Strong("Tipo: "), metric_type
                ], md=3),
                dbc.Col([
                    html.Strong("Unidades: "), units
                ], md=3),
                dbc.Col([
                    html.Strong("Días Máx: "), str(max_days)
                ], md=3)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Strong("Entidades disponibles: "),
                    html.Span(f"{', '.join(available_entities)}", className="text-muted")
                ], md=12)
            ], className="mt-2"),
            html.Hr(),
            html.P(description, className="mb-0")
        ])
    ], className="border-info")

# Callback simple para exportación directa a Excel
@app.callback(
    Output("export-status", "children"),
    [Input("simple-export-button", "n_clicks")],
    prevent_initial_call=True
)
def export_data_to_excel_simple(n_clicks):
    if not n_clicks:
        return dash.no_update
    
    try:
        print("=== SIMULANDO CLICK DEL BOTÓN DE EXPORTACIÓN ===")
        
        # Crear directorio de exportación (funciona tanto local como en producción)
        export_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generar nombre de archivo con timestamp
        timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DASHBOARD_TODAS_METRICAS_{timestamp}.xlsx"
        filepath = os.path.join(export_dir, filename)
        
        print(f"Archivo: {filename}")
        
        # Configurar fechas
        days_data = 30
        end_date = date.today()
        start_date = end_date - timedelta(days=days_data)
        
        total_metrics = len(todas_las_metricas)
        unique_metrics = todas_las_metricas['MetricId'].nunique()
        print(f"Total métricas en API: {total_metrics}")
        print(f"Métricas únicas: {unique_metrics}")
        print("🚀 EXPORTANDO TODAS LAS MÉTRICAS Y ENTIDADES...")
        
        # Crear archivo Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            
            # Hoja 1: Catálogo COMPLETO (todas las combinaciones)
            todas_las_metricas.to_excel(writer, sheet_name='Catálogo_COMPLETO', index=False)
            print(f"✓ Catálogo COMPLETO exportado ({total_metrics} combinaciones métrica-entidad)")
            
            # Procesar CADA combinación métrica-entidad individualmente
            exported_count = 0
            total_records = 0
            
            for index, (i, row) in enumerate(todas_las_metricas.iterrows(), 1):
                metric_id = row['MetricId']
                entity = row['Entity']
                metric_name = row['MetricName']
                
                print(f"({index}/{total_metrics}) {metric_id} - {entity}")
                
                try:
                    # Consultar datos para esta combinación específica
                    data = objetoAPI.request_data(metric_id, entity, start_date, end_date)
                    
                    if data is not None and not data.empty:
                        # Crear nombre de hoja válido (máximo 31 caracteres)
                        sheet_name = f"{metric_id}_{entity}"[:31]
                        # Limpiar caracteres especiales
                        invalid_chars = ['/', '\\', '[', ']', '*', '?', ':', "'", '"']
                        for char in invalid_chars:
                            sheet_name = sheet_name.replace(char, '_')
                        
                        # Exportar datos
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                        exported_count += 1
                        total_records += len(data)
                        
                        print(f"  ✓ {sheet_name}: {len(data)} registros, {len(data.columns)} columnas")
                    else:
                        print(f"  - Sin datos disponibles")
                
                except Exception as e:
                    print(f"  ✗ Error: {e}")
        
        # Resumen final
        print("\n✅ EXPORTACIÓN COMPLETA FINALIZADA")
        print(f"Archivo: {filename}")
        print(f"Combinaciones procesadas: {total_metrics}")
        print(f"Hojas de datos exportadas: {exported_count}")
        print(f"Total de registros: {total_records:,}")
        
        # Calcular tamaño del archivo
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"Tamaño: {file_size_mb:.2f} MB")
        
        return dash.no_update
    
    except Exception as e:
        print(f"ERROR CRÍTICO en exportación: {e}")
        import traceback
        traceback.print_exc()
        
        return dbc.Alert([
            html.I(className="bi bi-exclamation-triangle-fill me-2"),
            html.Strong("❌ Error en la exportación"),
            html.Br(), html.Br(),
            f"Error: {str(e)}",
            html.Br(),
            "Por favor revisa la consola para más detalles."
        ], color="danger", className="text-center")
        
        # Estadísticas finales
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        
        print(f"=== EXPORTACIÓN COMPLETA FINALIZADA ===")
        print(f"Archivo: {filename}")
        print(f"Métricas procesadas: {len(unique_metrics)}")
        print(f"Hojas de datos exportadas: {exported_count}")
        print(f"Total de registros: {total_records:,}")
        print(f"Tamaño del archivo: {file_size_mb:.2f} MB")
        print(f"Ubicación: {export_dir}")
        
        return dbc.Alert([
            html.I(className="bi bi-check-circle-fill me-2"),
            html.Strong("🎉 ¡EXPORTACIÓN COMPLETA FINALIZADA!"),
            html.Br(), html.Br(),
            html.Strong("📊 Estadísticas:"),
            html.Br(),
            f"📁 Archivo: {filename}",
            html.Br(),
            f"� Métricas procesadas: {len(unique_metrics)} de {total_metrics}",
            html.Br(),
            f"📋 Hojas exportadas: {exported_count}",
            html.Br(),
            f"📊 Total registros: {total_records:,}",
            html.Br(),
            f"💾 Tamaño: {file_size_mb:.2f} MB",
            html.Br(), html.Br(),
            f"📂 Ubicación: {export_dir}",
            html.Br(),
            html.Small("✅ Exportación SIN LÍMITES - Todos los datos disponibles en XM", className="text-success fw-bold")
        ], color="success", className="text-center", style={"fontSize": "0.9rem"})
        
    except Exception as e:
        print(f"ERROR CRÍTICO en exportación: {e}")
        import traceback
        traceback.print_exc()
        
        return dbc.Alert([
            html.I(className="bi bi-exclamation-triangle-fill me-2"),
            html.Strong("❌ Error en la exportación"),
            html.Br(), html.Br(),
            f"Error: {str(e)}",
            html.Br(),
            "Por favor revisa la consola para más detalles."
        ], color="danger", className="text-center")

# Callback principal para consultar y mostrar datos
@app.callback(
    [Output("tab-content", "children"),
     Output("loading-output", "children")],
    [Input("query-button", "n_clicks"),
     Input("tabs", "active_tab")],
    [dash.dependencies.State("metric-dropdown", "value"),
     dash.dependencies.State("entity-dropdown", "value"),
     dash.dependencies.State("start-date", "date"),
     dash.dependencies.State("end-date", "date")]
)
def update_content(n_clicks, active_tab, selected_metric, selected_entity, start_date, end_date):
    if not n_clicks or not selected_metric or not selected_entity:
        return dbc.Alert(
            "👆 Selecciona una métrica, entidad y fechas, luego haz clic en 'Consultar Datos'",
            color="info",
            className="text-center"
        ), ""
    
    try:
        # Convertir fechas
        start_dt = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Realizar consulta a la API
        data = objetoAPI.request_data(
            selected_metric,
            selected_entity,
            start_dt,
            end_dt
        )
        
        if data is None or data.empty:
            return dbc.Alert(
                "No se encontraron datos para los parámetros seleccionados.",
                color="warning"
            ), ""
        
        # Preparar contenido según la pestaña activa
        if active_tab == "table-tab":
            return create_data_table(data), ""
        elif active_tab == "line-chart-tab":
            return create_line_chart(data, selected_metric), ""
        elif active_tab == "bar-chart-tab":
            return create_bar_chart(data, selected_metric), ""
        elif active_tab == "stats-tab":
            return create_stats_summary(data), ""
        
    except Exception as e:
        return dbc.Alert(
            f"Error al consultar los datos: {str(e)}",
            color="danger"
        ), ""

def create_data_table(data):
    """Crear tabla interactiva con los datos"""
    return dbc.Card([
        dbc.CardHeader([
            html.H6([
                html.I(className="bi bi-table me-2"),
                f"Datos Consultados ({len(data)} registros)"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dash_table.DataTable(
                data=data.head(1000).to_dict('records'),  # Limitar a 1000 registros para rendimiento
                columns=[{"name": i, "id": i} for i in data.columns],
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data={
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                sort_action="native",
                filter_action="native",
                page_action="native",
                page_current=0,
                page_size=20,
                export_format="xlsx",
                export_headers="display"
            )
        ])
    ])

def create_line_chart(data, metric_name):
    """Crear gráfico de líneas"""
    # Detectar columna de fecha y valor
    date_cols = [col for col in data.columns if 'fecha' in col.lower() or 'date' in col.lower()]
    value_cols = [col for col in data.columns if col not in date_cols and data[col].dtype in ['float64', 'int64']]
    
    if not date_cols or not value_cols:
        return dbc.Alert("No se pueden crear gráficos con estos datos.", color="warning")
    
    date_col = date_cols[0]
    value_col = value_cols[0]
    
    fig = px.line(
        data, 
        x=date_col, 
        y=value_col,
        title=f"Evolución temporal: {metric_name}",
        labels={value_col: "Valor", date_col: "Fecha"}
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6([
                html.I(className="bi bi-graph-up me-2"),
                "Gráfico de Líneas"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig)
        ])
    ])

def create_bar_chart(data, metric_name):
    """Crear gráfico de barras"""
    # Detectar columnas categóricas y numéricas
    cat_cols = [col for col in data.columns if data[col].dtype == 'object']
    num_cols = [col for col in data.columns if data[col].dtype in ['float64', 'int64']]
    
    if not cat_cols or not num_cols:
        return dbc.Alert("No se pueden crear gráficos de barras con estos datos.", color="warning")
    
    cat_col = cat_cols[0]
    num_col = num_cols[0]
    
    # Agrupar datos si hay muchas categorías
    grouped_data = data.groupby(cat_col)[num_col].sum().reset_index()
    
    fig = px.bar(
        grouped_data.head(20),  # Top 20 para mejor visualización
        x=cat_col,
        y=num_col,
        title=f"Distribución por categoría: {metric_name}",
        labels={num_col: "Valor", cat_col: "Categoría"}
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6([
                html.I(className="bi bi-bar-chart me-2"),
                "Gráfico de Barras"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig)
        ])
    ])

def create_stats_summary(data):
    """Crear resumen estadístico"""
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    
    if numeric_data.empty:
        return dbc.Alert("No hay datos numéricos para análisis estadístico.", color="warning")
    
    stats = numeric_data.describe()
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6([
                html.I(className="bi bi-calculator me-2"),
                "Resumen Estadístico"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dash_table.DataTable(
                data=stats.round(2).reset_index().to_dict('records'),
                columns=[{"name": i, "id": i} for i in stats.reset_index().columns],
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data={
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            )
        ])
    ])

if __name__ == "__main__":
    import os
    # Para producción (Heroku, Railway, etc.)
    port = int(os.environ.get("PORT", 8052))
    debug_mode = os.environ.get("DASH_DEBUG", "True").lower() == "true"
    
    app.run(
        debug=debug_mode, 
        host="0.0.0.0", 
        port=port
    )
