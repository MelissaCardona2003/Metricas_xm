# 📊 Dashboard Energía XM Colombia

Dashboard interactivo para visualizar y exportar datos del mercado energético colombiano usando la API de XM.

## 🌟 Características

- ✅ **190 métricas** del mercado energético colombiano
- ✅ **Visualizaciones interactivas** con Plotly
- ✅ **Exportación completa** a Excel sin límites
- ✅ **Interfaz moderna** con Bootstrap
- ✅ **Responsive** para móviles y desktop

## � Ejecutar Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

## � Estructura del Proyecto

```
├── app.py                 # Aplicación principal
├── config.py             # Configuración
├── requirements.txt      # Dependencias Python
├── Procfile             # Configuración Heroku
├── runtime.txt          # Versión Python para Heroku
└── exports/             # Archivos Excel exportados
```

## 🌐 Variables de Entorno

- `PORT`: Puerto del servidor (automático en producción)
- `DASH_DEBUG`: Modo debug (false en producción)

## 📊 Funcionalidades

### Consulta de Datos
- Selecciona métrica y entidad
- Configura rango de fechas
- Visualiza en tabla o gráfico

### Exportación Completa
- **190 métricas** sin límites
- Todas las combinaciones métrica-entidad
- Exportación directa a Excel
- Datos idénticos a la API de XM

## 🛠 Tecnologías

- **Dash**: Framework web
- **Plotly**: Visualizaciones
- **Pandas**: Manipulación de datos
- **pydataxm**: API de XM Colombia
- **Bootstrap**: UI moderna

## 📝 Autor

Dashboard creado para el análisis del mercado energético colombiano.

---

🚀 **¡Tu dashboard estará disponible en una URL pública!**
# Metricas_xm
