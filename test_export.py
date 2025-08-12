#!/usr/bin/env python3

import sys
sys.path.append('/home/melissa/Documentos/dashboard-energia-xm/API_XM')
from pydataxm.pydataxm import ReadDB
import pandas as pd
from datetime import date, timedelta
import datetime as dt
import os

def test_complete_export():
    print("=== SIMULANDO CLICK DEL BOTÓN DE EXPORTACIÓN ===")
    
    try:
        # Exactamente el mismo código del callback
        export_dir = "/home/melissa/Documentos/MME/Utlidades del proyecto 1/dashboard-energia-xm/exports"
        os.makedirs(export_dir, exist_ok=True)
        
        timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MANUAL_TEST_TODAS_METRICAS_{timestamp}.xlsx"
        filepath = os.path.join(export_dir, filename)
        
        print(f"Archivo: {filename}")
        
        # Inicializar API
        objetoAPI = ReadDB()
        todas_las_metricas = objetoAPI.get_collections()
        
        days_data = 30
        end_date = date.today()
        start_date = end_date - timedelta(days=days_data)
        
        print(f"Total métricas en API: {len(todas_las_metricas)}")
        unique_metrics = todas_las_metricas['MetricId'].unique()
        print(f"Métricas únicas: {len(unique_metrics)}")
        
        # PROCESAR TODAS LAS MÉTRICAS SIN LÍMITES
        print("🚀 EXPORTANDO TODAS LAS MÉTRICAS Y ENTIDADES...")
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            
            # Catálogo completo (todas las 190 combinaciones)
            todas_las_metricas.to_excel(writer, sheet_name='Catálogo_COMPLETO', index=False)
            print("✓ Catálogo COMPLETO exportado (190 combinaciones métrica-entidad)")
            
            exported_count = 0
            total_records = 0
            
            # PROCESAR CADA FILA DEL CATÁLOGO (TODAS LAS 190 COMBINACIONES)
            for i, (_, row) in enumerate(todas_las_metricas.iterrows()):
                metric_id = row['MetricId']
                entity = row['Entity']
                metric_name = row['MetricName']
                
                print(f"({i+1}/{len(todas_las_metricas)}) {metric_id} - {entity}")
                
                try:
                    if pd.isna(entity):
                        print(f"  - Entidad vacía, saltando...")
                        continue
                    
                    # Consultar datos para esta combinación específica
                    data = objetoAPI.request_data(metric_id, entity, start_date, end_date)
                    
                    if data is not None and not data.empty:
                        # Crear nombre de hoja único
                        sheet_name = f"{metric_id}_{entity}"[:31]
                        # Limpiar caracteres especiales
                        for char in ['/', '\\', '[', ']', '*', '?', ':', "'", '"']:
                            sheet_name = sheet_name.replace(char, '_')
                        
                        # Asegurar nombres únicos de hojas
                        original_name = sheet_name
                        counter = 1
                        existing_names = [sheet for sheet in writer.sheets.keys()]
                        while sheet_name in existing_names:
                            sheet_name = f"{original_name[:28]}_{counter:02d}"
                            counter += 1
                        
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                        exported_count += 1
                        total_records += len(data)
                        print(f"  ✓ {sheet_name}: {len(data)} registros, {len(data.columns)} columnas")
                    else:
                        print(f"  - Sin datos disponibles")
                
                except Exception as e:
                    print(f"  ✗ Error: {e}")
        
        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        print(f"\n✅ EXPORTACIÓN COMPLETA FINALIZADA")
        print(f"Archivo: {filename}")
        print(f"Combinaciones procesadas: {len(todas_las_metricas)}")
        print(f"Hojas de datos exportadas: {exported_count}")
        print(f"Total de registros: {total_records:,}")
        print(f"Tamaño: {file_size:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_export()
    exit(0 if success else 1)
