# 📊 Dashboard Energía XM Colombia

Dashboard interactivo para visualizar y exportar datos del mercado energético colombiano usando la API de XM.

## 🌟 Características

- ✅ **190 métricas** del mercado energético colombiano
- ✅ **Visualizaciones interactivas** con Plotly
- ✅ **Exportación completa** a Excel sin límites
- ✅ **Interfaz moderna** con Bootstrap
- ✅ **Responsive** para móviles y desktop

## 🚀 Despliegue en la Nube

### Heroku (Recomendado)

1. **Crea cuenta en Heroku**: https://heroku.com
2. **Instala Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Clona este repositorio**
4. **Ejecuta estos comandos**:

```bash
# Inicializar git (si no está)
git init
git add .
git commit -m "Dashboard XM Colombia"

# Crear app en Heroku
heroku create tu-dashboard-xm-colombia

# Configurar variables de entorno para producción
heroku config:set DASH_DEBUG=false

# Desplegar
git push heroku main
```

### Railway.app

1. Conecta tu GitHub en: https://railway.app
2. Selecciona este repositorio
3. ¡Railway despliega automáticamente!

### Render.com

1. Conecta GitHub en: https://render.com
2. Crea un "Web Service"
3. Usa estos settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

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
