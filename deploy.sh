#!/bin/bash

echo "🚀 Preparando Dashboard XM para Despliegue"
echo "=========================================="

# Inicializar Git si no existe
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositorio Git..."
    git init
else
    echo "📁 Repositorio Git ya existe"
fi

# Agregar todos los archivos
echo "📦 Agregando archivos..."
git add .

# Hacer commit
echo "💾 Creando commit..."
git commit -m "Dashboard XM Colombia - Listo para despliegue" || echo "No hay cambios que commitear"

echo ""
echo "✅ ¡Preparación completa!"
echo ""
echo "🌐 OPCIONES DE DESPLIEGUE:"
echo ""
echo "1️⃣  HEROKU (Recomendado):"
echo "   heroku create tu-dashboard-xm"
echo "   heroku config:set DASH_DEBUG=false"
echo "   git push heroku main"
echo ""
echo "2️⃣  RAILWAY:"
echo "   Sube a GitHub y conecta en railway.app"
echo ""
echo "3️⃣  RENDER:"
echo "   Sube a GitHub y conecta en render.com"
echo ""
echo "🔗 Después tendrás una URL pública como:"
echo "   https://tu-dashboard-xm.herokuapp.com"
echo "   https://tu-dashboard-xm.up.railway.app"
echo "   https://tu-dashboard-xm.onrender.com"
