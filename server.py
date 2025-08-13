#!/usr/bin/env python3
"""
Servidor Flask para Dashboard Energético XM Colombia
Sirve la aplicación Dash sobre un servidor Flask robusto
"""

import os
from flask import Flask, redirect, url_for
from app import app as dash_app
from waitress import serve
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener el servidor Flask de la app Dash
server = dash_app.server

# Configurar Flask
server.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'xm-dashboard-secret-key-2025'),
    DEBUG=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
)

# Rutas adicionales de Flask
@server.route('/')
def index():
    """Redirigir a la aplicación Dash"""
    return redirect('/_dash-layout')

@server.route('/health')
def health_check():
    """Health check endpoint para monitoreo"""
    return {
        'status': 'healthy',
        'service': 'Dashboard XM Colombia',
        'version': '1.0.0'
    }

@server.route('/info')
def app_info():
    """Información de la aplicación"""
    return {
        'name': 'Dashboard Energético XM Colombia',
        'description': 'Dashboard interactivo para métricas energéticas de XM',
        'metrics_available': 190,
        'features': [
            'Visualización de 190 métricas energéticas',
            'Exportación completa a Excel',
            'Interfaz responsive',
            'Datos en tiempo real de XM'
        ]
    }

def create_app():
    """Factory function para crear la aplicación"""
    return server

if __name__ == '__main__':
    # Configuración del puerto y host
    port = int(os.environ.get('PORT', 8052))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Iniciando Dashboard XM en http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    
    if debug:
        # Modo desarrollo - usar servidor de desarrollo Flask
        server.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    else:
        # Modo producción - usar Waitress (servidor WSGI robusto)
        logger.info("🏭 Usando servidor Waitress para producción")
        serve(
            server,
            host=host,
            port=port,
            threads=4,
            connection_limit=1000,
            cleanup_interval=30,
            channel_timeout=120
        )
